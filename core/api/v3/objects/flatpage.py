from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.flatpages.models import FlatPage
from rest_framework import permissions, serializers

from .base import BaseProvider


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = FlatPage
        exclude = [
            "sites",
            "enable_comments",
            "template_name",
        ]  # fields = all - sites, enable_comments, template_name


class FlatPageProvider(BaseProvider):
    model = FlatPage
    allow_list = True
    additional_lookup_fields = ["url"]
    raw_serializers = {
        "_": Serializer,
    }

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
