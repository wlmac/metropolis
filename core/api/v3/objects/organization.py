from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from rest_framework import permissions, serializers

from core import models
from core.api.serializers.custom import MembersField, TagRelatedField

from .base import BaseProvider


class Serializer(serializers.ModelSerializer):
    tags = TagRelatedField()
    followers = MembersField()
    execs = MembersField()
    supervisors = MembersField()
    owners = MembersField()

    links = serializers.SlugRelatedField(
        slug_field="url",
        many=True,
        queryset=models.OrganizationURL.objects.all(),
    )

    class Meta:
        model = models.Organization
        fields = "__all__"

    def get_fields(self):
        # mirror OrganizationAdmin.get_readonly_fields; links/followers are never set from here
        # (links is a reverse FK, so setting it would move another club's links onto this one)
        fields = super().get_fields()
        locked = {"links", "followers"}
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not (user and user.is_superuser):
            locked |= {"owners", "slug", "supervisors", "is_active"}
            if not (
                isinstance(self.instance, models.Organization)
                and self.instance.owners.filter(pk=user.pk).exists()
            ):
                locked.add("execs")
        for name in locked & fields.keys():
            fields[name].read_only = True
        return fields

    def validate(self, attrs):
        execs = attrs.get("execs")
        if execs is not None and self.instance is not None:
            owners = attrs.get("owners", self.instance.owners.all())
            if any(o not in execs for o in owners):
                raise serializers.ValidationError(
                    {"execs": "The owner must also be an exec."}
                )
        return attrs


class SupervisorOrExec(permissions.BasePermission):
    def has_object_permission(self, request, view, organization):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user in organization.supervisors.all()
            or request.user in organization.execs.all()
        )


class OrganizationProvider(BaseProvider):
    model = models.Organization
    allow_new = False
    listing_filters = {
        "tags": int,
        "owners": int,
        "supervisors": int,
        "execs": int,
        "is_active": bool,
    }
    additional_lookup_fields = ["slug"]
    raw_serializers = {
        "_": Serializer,
    }

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
            .annotate(num_followers=Count("follower"))
            .order_by("-num_followers")
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
