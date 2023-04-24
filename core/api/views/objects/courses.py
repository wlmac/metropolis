from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, serializers

from core.models import Course
from .base import BaseProvider


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in ('GET', 'HEAD', 'OPTIONS')


class Serializer(serializers.ModelSerializer):
    position = serializers.IntegerField(min_value=1, max_value=4)

    class Meta:
        model = Course
        fields = ["id", "code", "description", "position"]


class CreateSerializer(Serializer):
    class Meta:
        model = Course
        fields = ["id", "code", "description", "position", "term"]


class CourseProvider(BaseProvider):
    model = Course
    allow_single = False
    listing_filters = ["term", "position"]

    @property
    def serializer_class(self):
        return CreateSerializer if self.request.kind == "new" else Serializer

    @property
    def permission_classes(self):
        if self.request.kind == "new":
            return [permissions.AllowAny]
        return [ReadOnly]

    def get_listing_queryset(self, request):
        query_params = request.query_params
        filters = {}
        for lookup_filter, lookup_value in query_params.items():
            if lookup_filter in self.listing_filters:
                filters[lookup_filter] = int(lookup_value)

        if filters:
            return Course.objects.filter(**filters).order_by("position")

        return Course.objects.order_by("term")

    def get_queryset(self, request):
        if self.request.kind == "list":
            return self.get_listing_queryset(request)
        return Course.objects.all()

    def get_last_modified(self, view):
        return view.get_object().last_modified_date

    def get_last_modified_queryset(self):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="course")
            )
            .latest("action_time")
            .action_time
        )
