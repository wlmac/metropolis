from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.flatpages.models import FlatPage
from rest_framework import generics, permissions, serializers

from .base import BaseProvider


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = FlatPage
        fields = "__all__"


class Provider(BaseProvider):
    serializer_class = Serializer
    model = FlatPage
    allow_list = False
    lookup_field = "url"

    @property
    def permission_classes(self):
        return (
            [permissions.DjangoModelPermissions]
            if self.request.mutate
            else [permissions.AllowAny]
        )

    def get_queryset(self, request):
        return FlatPage.objects.all()

    def get_last_modified(self, view):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(
                    app_label="flatpages", model="flatpage"
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
                    app_label="flatpages", model="flatpage"
                )
            )
            .latest("action_time")
            .action_time
        )
