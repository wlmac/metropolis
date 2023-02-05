from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework import permissions, serializers

from core.utils.mail import send_mail
from .base import BaseProvider
from ...utils import ModelAbilityField, PrimaryKeyRelatedAbilityField
from ....models import Announcement, Organization, User


class SupervisorField(PrimaryKeyRelatedAbilityField):
    def get_queryset(self):
        request = self.context.get("request", None)
        if not request.user.is_authenticated:
            return User.objects.none()
        orgs = Organization.objects.filter(
            Q(supervisors=request.user) | Q(execs=request.user)
        )
        return User.objects.filter(organizations_supervising__in=orgs)


class ExecEtcSerializer(serializers.ModelSerializer):
    supervisor = SupervisorField("edit", queryset=User.all())
    message = serializers.CharField(read_only=True)

    def save(self, *args, **kwargs):
        notify_supervisors = False

        obj = super().save(*args, **kwargs)

        user = self.context["request"].user
        # if not user.is_superuser:
        if True:
            if user in obj.organization.supervisors.all():
                obj.supervisor = user
                if obj.status not in {"d", "p"} and user != obj.author:
                    # Notify author
                    obj.message = f"Successfully marked announcement as {obj.get_status_display()}."
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
        fields = "__all__"
        read_only_fields = ["status", "rejection_reason"]


class SupervisorSerializer(serializers.ModelSerializer):
    supervisor = SupervisorField("edit", queryset=User.all())
    status = ModelAbilityField(
        "approve", model_field=Announcement()._meta.get_field("status")
    )
    rejection_reason = ModelAbilityField(
        "approve", model_field=Announcement()._meta.get_field("rejection_reason")
    )

    class Meta:
        model = Announcement
        fields = "__all__"


class Inner(permissions.BasePermission):
    def has_object_permission(self, request, view, ann):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.can_edit(ann):
            return True
        return False


class Provider(BaseProvider):
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
        return ExecEtcSerializer

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
