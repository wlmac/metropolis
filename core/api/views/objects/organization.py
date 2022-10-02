from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions
from rest_framework import serializers

from .base import BaseProvider
from .... import models


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = "__all__"


class Provider(BaseProvider):
    serializer_class = Serializer
    model = models.Organization

    @property
    def permission_classes(self):
        return [permissions.DjangoModelPermissions] if self.request.mutate else [permissions.AllowAny]

    def get_queryset(self, request):
        return models.Organization.objects.all()

    def get_last_modified(self, view):
        return LogEntry.objects \
            .filter(content_type=ContentType.objects.get(app_label='core', model='organization')) \
            .filter(object_id=str(view.get_object().pk)) \
            .latest('action_time') \
            .action_time

    def get_last_modified_queryset(self):
        return LogEntry.objects \
            .filter(content_type=ContentType.objects.get(app_label='core', model='organization')) \
            .latest('action_time') \
            .action_time

