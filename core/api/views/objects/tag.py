from django.db.models import Q
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework import serializers

from .... import models
from .base import BaseProvider


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ["id", "name", "color"]

class Provider(BaseProvider):
    model = models.Tag
    serializer_class = Serializer

    @property
    def permission_classes(self):
        return [permissions.DjangoModelPermissions] if self.request.mutate else [permissions.AllowAny]

    def get_queryset(self, request):
        return models.Tag.objects.all()

    def get_last_modified(self, view):
        return LogEntry.objects \
            .filter(content_type=ContentType.objects.get(app_label='core', model='tag')) \
            .filter(object_id=str(view.get_object().pk)) \
            .latest('action_time') \
            .action_time

    def get_last_modified_queryset(self):
        return LogEntry.objects \
            .filter(content_type=ContentType.objects.get(app_label='core', model='tag')) \
            .latest('action_time') \
            .action_time

