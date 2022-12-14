from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, permissions, serializers

from .... import models
from .base import BaseProvider


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ["id", "name", "color"]
        read_only_fields = ["color"]


class Inner(permissions.BasePermission):
    def has_object_permission(self, request, view, tag):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.can_edit(tag):
            return True
        return False


class Provider(BaseProvider):
    model = models.Tag
    serializer_class = Serializer

    @property
    def permission_classes(self):
        return (
            [permissions.DjangoModelPermissions | Inner]
            if self.request.mutate
            else [permissions.AllowAny]
        )

    def get_queryset(self, request):
        return models.Tag.objects.all()

    def get_last_modified(self, view):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="tag")
            )
            .filter(object_id=str(view.get_object().pk))
            .latest("action_time")
            .action_time
        )

    def get_last_modified_queryset(self):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="tag")
            )
            .latest("action_time")
            .action_time
        )
