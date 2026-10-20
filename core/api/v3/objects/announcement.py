from __future__ import annotations

from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from rest_framework import permissions, serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from core.api.serializers.custom import (
    LikeField,
    OrganizationField,
    SingleUserField,
    TagRelatedField,
)
from core.models import Announcement
from core.utils.mail import send_mail

from .base import BaseProvider


def exec_validator(value):
    if value not in {"d", "p"}:
        raise ValidationError("only draft or pending allowed", code="exec")


class OrgAccessMixin:
    """Creating or moving an item needs rights on the target organization."""

    def validate(self, attrs):
        user = self.context["request"].user
        if user.is_superuser:
            return super().validate(attrs)
        if self.instance is None or "organization" in attrs:
            org = attrs.get("organization")
            if org is None or user not in (
                org.owners.all() | org.execs.all() | org.supervisors.all()
            ):  # no organization (global) is superuser only
                raise PermissionDenied("not allowed to post for this organization")
        if "author" in attrs:
            old = getattr(self.instance, "author", None)
            if attrs["author"] != (old if self.instance else user):
                raise PermissionDenied("author must be yourself")
        return super().validate(attrs)


class Serializer(OrgAccessMixin, serializers.ModelSerializer):
    message = serializers.CharField(read_only=True)
    likes = LikeField()
    tags = TagRelatedField()
    author = SingleUserField()
    organization = OrganizationField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self._is_supervisor():
            # only supervisors may reject or assign a supervisor
            self.fields["supervisor"].read_only = True
            self.fields["rejection_reason"].read_only = True

    def _is_supervisor(self, org=None):
        user = self.context["request"].user
        if isinstance(
            self.instance, Announcement
        ):  # always the instance's org, not the incoming
            org = self.instance.organization
        return user.is_superuser or (org is not None and user in org.supervisors.all())

    def save(self, **kwargs):
        notify_supervisors = False
        user = self.context["request"].user
        incoming_status = self.validated_data.get(
            "status", getattr(self.instance, "status", "p")
        )
        is_supervisor = self._is_supervisor(self.validated_data.get("organization"))
        if not is_supervisor:  # only supervisors can approve/reject, so persist d or p
            kwargs["status"] = "d" if incoming_status == "d" else "p"
        if is_supervisor:
            kwargs["supervisor"] = user
        obj: Announcement = super().save(**kwargs)
        if is_supervisor:
            if obj.status not in {"d", "p"} and user != obj.author:
                obj.message = (
                    f"Successfully marked announcement as {obj.get_status_display()}."
                )
        elif incoming_status not in ("d", "p"):
            notify_supervisors = True
            if incoming_status != "a":
                obj.message = "Successfully sent announcement for review."

        if notify_supervisors:
            for teacher in obj.organization.supervisors.all():
                email_template_context = {
                    "teacher": teacher,
                    "announcement": obj,
                    "review_link": settings.SITE_URL
                    + reverse("admin:core_announcement_change", args=(obj.pk,)),
                }

                send_mail(
                    f"【{obj.organization.name}】Announcement Approval Requested: {obj.title}",
                    render_to_string(
                        "core/email/verify_announcement.txt",
                        email_template_context,
                    ),
                    None,
                    [teacher.email],
                    bcc=settings.ANNOUNCEMENT_APPROVAL_BCC_LIST,
                    html_message=render_to_string(
                        "core/email/verify_announcement.html",
                        email_template_context,
                    ),
                )
        return obj

    class Meta:
        model = Announcement
        fields = [
            "id",
            "created_date",
            "last_modified_date",
            "show_after",
            "title",
            "body",
            "is_public",
            "status",
            "rejection_reason",
            "author",
            "organization",
            "organization_string",
            "supervisor",
            "tags",
            "likes",
            "message",
        ]


class OneSerializer(Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self._is_supervisor():
            self.fields["status"].validators.append(exec_validator)


class Inner(permissions.BasePermission):
    def has_object_permission(self, request, view, ann):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.can_edit(ann)


class AnnouncementProvider(BaseProvider):
    model = Announcement
    listing_filters = {
        "tags": [(int, ""), (str, "name")],
        "organization": int,
        "author": int,
        "last_modified_date__gt": str,
        "last_modified_date__gte": str,
        "last_modified_date__lt": str,
        "last_modified_date__lte": str,
    }
    raw_serializers = {
        "single": OneSerializer,
        "retrieve": OneSerializer,
        "_": Serializer,
    }

    @property
    def permission_classes(self):
        return (
            [permissions.DjangoModelPermissions, Inner]
            if self.request.mutate
            else [permissions.AllowAny]
        )

    @staticmethod
    def get_queryset(request):
        return Announcement.get_all(request.user)

    @staticmethod
    def get_last_modified(view):
        return view.get_object().last_modified_date

    @staticmethod
    def get_last_modified_queryset():
        last_modified_date = (
            Announcement.objects.all().order_by("-last_modified_date", "id").first()
        )

        if last_modified_date:
            return timezone.localtime(last_modified_date.last_modified_date)
        else:
            return timezone.localtime(timezone.now())
