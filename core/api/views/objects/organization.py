from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, serializers

from .base import BaseProvider
from .... import models


class Serializer(serializers.ModelSerializer):
    links = serializers.SlugRelatedField(
        slug_field="url", many=True, queryset=models.OrganizationURL.objects.all()
    )
    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.User.objects.all()
    )

    class Meta:
        model = models.Organization
        fields = "__all__"


class SupervisorOrExec(permissions.BasePermission):
    def has_object_permission(self, request, view, organization):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user in {*organization.supervisors} | {*org.execs}:
            return True
        return False


class Provider(BaseProvider):
    serializer_class = Serializer
    model = models.Organization
    allow_new = False

    @property
    def permission_classes(self):
        return (
            [permissions.DjangoModelPermissions, SupervisorOrExec]
            if self.request.mutate
            else [permissions.AllowAny]
        )

    def get_queryset(self, request):
        return models.Organization.objects.filter(is_active=True)

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
