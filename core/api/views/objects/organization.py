from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from rest_framework import permissions, serializers

from core.api.utils.gravatar import gravatar_url
from core.models import Tag, User, Organization, Comment

from .base import BaseProvider
from .... import models


class Serializer(serializers.ModelSerializer):
    gravatar_url = serializers.SerializerMethodField(read_only=True)
    links = serializers.SlugRelatedField(
        slug_field="url", many=True, queryset=models.OrganizationURL.objects.all()
    )
    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.User.objects.all()
    )

    class Meta:
        model = models.Organization
        fields = ["id", "username", "first_name", "last_name", "organization", "gravatar_url"]

    @staticmethod
    def get_gravatar_url(obj: Organization):
        return gravatar_url(obj.organization)


class SupervisorOrExec(permissions.BasePermission):
    def has_object_permission(self, request, view, organization):
        if request.method in permissions.SAFE_METHODS:
            return True
        if (
            request.user in organization.supervisors.all()
            or request.user in organization.execs.all()
        ):
            return True
        return False


class OrganizationProvider(BaseProvider):
    serializer_class = Serializer
    model = models.Organization
    allow_new = False
    listing_filters = {
        "tags": int,
        "owner": int,
        "supervisors": int,
        "execs": int,
        "is_active": bool,
        "is_open": bool,
    }
    lookup_fields = ["id", "slug"]

    @property
    def permission_classes(self):
        return (
            [permissions.DjangoModelPermissions, SupervisorOrExec]
            if self.request.mutate
            else [permissions.AllowAny]
        )

    def get_queryset(self, request):
        return (
            models.Organization.objects.filter(is_active=True)
            .annotate(num_members=Count("member"))
            .order_by("-num_members")
        )

    def get_last_modified(self, view):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(
                    app_label="core", model="organization"
                )
            )
            .filter(object_id=str(view.get_object().pk))
            .latest("action_time")
            .action_time
        )

    def get_last_modified_queryset(self):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(
                    app_label="core", model="organization"
                )
            )
            .latest("action_time")
            .action_time
        )
