from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from rest_framework import permissions, serializers

from .base import BaseProvider
from ...serializers.custom import TagRelatedField, MembersField, AuthorField
from .... import models
from ....models import Organization


class Serializer(serializers.ModelSerializer):
    tags = TagRelatedField()
    members = MembersField()
    execs = MembersField()
    supervisors = MembersField()
    owner = AuthorField()


    links = serializers.SlugRelatedField(
        slug_field="url", many=True, queryset=models.OrganizationURL.objects.all()
    )

    def to_representation(self, instance: Organization):
        request = self.context["request"]
        if (
                request.mutate is False and request.detail
        ):  # detail is True and mutate is False meaning we are retrieving an object
            instance.increment_views()
        return super().to_representation(instance)

    class Meta:
        model = Organization
        fields = "__all__"


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
    model = Organization
    allow_new = False
    '''listing_filters = {
        "tags": int,
        "owner": int,
        "supervisors": int,
        "execs": int,
        "is_active": bool,
        "is_open": bool,
    }'''
    additional_lookup_fields = ["slug"]

    @property
    def permission_classes(self):
        return (
            [permissions.DjangoModelPermissions, SupervisorOrExec]
            if self.request.mutate
            else [permissions.AllowAny]
        )

    '''def get_queryset(self, request):
        return (
            models.Organization.objects.filter(is_active=True)
            .annotate(num_members=Count("member"))
            .order_by("-num_members")
        )'''

    def get_queryset(self, request):
        if request.user.has_perm("core.organization.view") or request.user.is_superuser:
            return Organization.objects.filter()

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
