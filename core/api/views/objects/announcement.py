from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Case, BooleanField, When, Q
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework import permissions, serializers
from rest_framework.exceptions import ValidationError

from core.utils.mail import send_mail

from ....models import Announcement, Organization, User
from ...utils import ModelAbilityField, PrimaryKeyRelatedAbilityField
from .base import BaseProvider


class SupervisorField(PrimaryKeyRelatedAbilityField):
    def get_queryset(self):
        request = self.context.get("request", None)
        if not request.user.is_authenticated:
            return User.objects.none()
        orgs = Organization.objects.filter(
            Q(supervisors=request.user) | Q(execs=request.user)
        )
        return User.objects.filter(organizations_supervising__in=orgs)


def exec_validator(value, serializer_field):
    if value not in {"d", "p"}:
        raise ValidationError("only draft or pending allowed", code="exec")


def always_fail_validator(value, serializer_field):
    raise ValidationError("always fail", code="exec")


class Serializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    def get_likes(self, obj: Announcement) -> int:
        return obj.likes.count()

    def get_comments(self, obj: Announcement) -> list[dict[str, bool]]:
        if (
            self.context["request"].user.has_perm("core.comment.view_flagged")
            or self.context["request"].user.is_staff
        ):
            comments = (
                obj.comments.all()
                .annotate(
                    child_count=Count("children"),
                    has_children=Case(
                        When(child_count__gt=0, then=True),
                        default=False,
                        output_field=BooleanField(),
                    ),
                )
                .values("id", "has_children")
            )

        else:
            comments = (
                obj.comments.filter(live=True)
                .annotate(
                    child_count=Count("children"),
                    has_children=Case(
                        When(child_count__gt=0, then=True),
                        default=False,
                        output_field=BooleanField(),
                    ),
                )
                .values("id", "has_children")
            )
        return comments

    def save(self, *args, **kwargs):
        notify_supervisors = False
        obj = super().save(*args, **kwargs)
        user = self.context["request"].user
        if user in obj.organization.supervisors.all():
            obj.supervisor = user
            if obj.status not in {"d", "p"} and user != obj.author:
                obj.message = (
                    f"Successfully marked announcement as {obj.get_status_display()}."
                )
        else:
            if obj.status not in ("d", "p"):
                notify_supervisors = True

                obj.message = f"Successfully sent announcement for review."
            obj.status = "p" if obj.status != "d" else "d"

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
            "supervisor",
            "tags",
            "likes",
            "comments",
        ]


class OneSerializer(Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        # these HiddenFields should never be used to set values
        self.status = serializers.HiddenField(
            default="", validators=[always_fail_validator]
        )
        self.rejection_reason = serializers.HiddenField(
            default="", validators=[always_fail_validator]
        )
        instance = self.instance
        if instance:
            if user in instance.organization.supervisors.all():
                self.supervisor = SupervisorField(
                    "edit", queryset=User.objects.filter(is_teacher=True)
                )
                self.status = ModelAbilityField(
                    "approve", model_field=Announcement()._meta.get_field("status")
                )
                self.rejection_reason = ModelAbilityField(
                    "approve",
                    model_field=Announcement()._meta.get_field("rejection_reason"),
                )
            elif user in instance.organization.execs.all():
                self.supervisor = SupervisorField(
                    "edit", queryset=User.objects.filter(is_teacher=True)
                )
                self.status = serializers.CharField(validators=[exec_validator])
                self.rejection_reason = serializers.CharField(read_only=True)


class Inner(permissions.BasePermission):
    def has_object_permission(self, request, view, ann):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.can_edit(ann):
            return True
        return False


class AnnouncementProvider(BaseProvider):
    model = Announcement

    @property
    def permission_classes(self):
        return (
            [permissions.DjangoModelPermissions, Inner]
            if self.request.mutate
            else [permissions.AllowAny]
        )

    @property
    def serializer_class(self):
        return (
            OneSerializer if self.request.kind in ("single", "retrieve") else Serializer
        )

    def get_queryset(self, request):
        return Announcement.get_all(request.user)

    def get_last_modified(self, view):
        return view.get_object().last_modified_date

    def get_last_modified_queryset(self):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(
                    app_label="core", model="announcement"
                )
            )
            .latest("action_time")
            .action_time
        )
