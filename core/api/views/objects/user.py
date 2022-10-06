from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework import serializers

from .... import models
from .base import BaseProvider


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "bio",
            "timezone",
            "graduating_year",
            "organizations",
            "tags_following",
        ]


class Identity(permissions.BasePermission):
    def has_object_permission(self, request, view, user):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user == user:
            return True
        return False


class Provider(BaseProvider):
    serializer_class = Serializer
    model = models.User
    allow_list = False

    @property
    def permission_classes(self):
        return [Identity] if self.request.mutate else [permissions.IsAuthenticated]

    def get_queryset(self, request):
        return models.User.objects.all()

    def get_last_modified(self, view):
        return timezone.now()

    def get_last_modified_queryset(self):
        return timezone.now()
