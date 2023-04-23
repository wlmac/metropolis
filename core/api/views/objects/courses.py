from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions

from core.models import Course
from .base import BaseProvider
from ...serializers import CourseSerializer


class CourseProvider(BaseProvider):
    serializer_class = CourseSerializer
    model = Course
    allow_single = False
    listing_filters = ["term", 'position']

    @property
    def permission_classes(self):
        return (
            [permissions.DjangoModelPermissions]
            if self.request.mutate
            else [permissions.AllowAny]
        )

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
