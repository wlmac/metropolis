from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, permissions
from rest_framework import serializers

from ....models import Announcement
from .base import BaseProvider


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        exclude = ["supervisor", "status", "rejection_reason"]


class SupervisorOrExec(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user in {*(org := obj.organization).supervisors} | {*org.execs}:
            return True
        return False


class Provider(BaseProvider):
    serializer_class = Serializer
    model = Announcement

    @property
    def permission_classes(self):
        return [permissions.DjangoModelPermissions, SupervisorOrExec] if self.request.mutate else [permissions.AllowAny]

    def get_queryset(self, request):
        return Announcement.get_all(request.user)

    def get_last_modified(self, view):
        return view.get_object().last_modified_date

    def get_last_modified_queryset(self):
        return LogEntry.objects \
            .filter(content_type=ContentType.objects.get(app_label='core', model='announcement')) \
            .latest('action_time') \
            .action_time
