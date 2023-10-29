from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, serializers

from core.models import Course
from .base import BaseProvider


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in ("GET", "HEAD", "OPTIONS")


class Serializer(serializers.ModelSerializer):
    position = serializers.IntegerField(min_value=1, max_value=6)  # 5,6 are for spares.

    class Meta:
        model = Course
        fields = ["id", "code", "description", "position"]


class CreateSerializer(Serializer):
    class Meta:
        model = Course
        fields = ["id", "code", "description", "position", "term"]

    def create(self, validated_data):
        if Course.objects.filter(
            code=validated_data["code"], term=validated_data["term"]
        ).exists():
            raise serializers.ValidationError("Course already exists")
        return super().create(validated_data)


class CourseProvider(BaseProvider):
    model = Course
    allow_single = False
    listing_filters = {"term": int, "position": int}

    @property
    def serializer_class(self):
        return CreateSerializer if self.request.kind == "new" else Serializer

    @property
    def permission_classes(self):
        if self.request.kind == "new":
            return [permissions.AllowAny]
        return [ReadOnly]

    def get_queryset(self, request):
        return Course.objects.all().order_by("term", "position").reverse()

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
