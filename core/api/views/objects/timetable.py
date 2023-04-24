from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework import permissions, serializers

from .base import BaseProvider
from ...serializers.course import CourseSerializer, TermSerializer
from ....models import Timetable


class ViewSerializer(serializers.ModelSerializer):
    term = TermSerializer()
    courses = CourseSerializer(many=True)
    class Meta:
        model = Timetable
        ordering = ["-term__start_date"]
        fields = ["term", "courses"]


class MutateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        ordering = ["-term__start_date"]
        fields = ["term", "courses"]


class Identity(permissions.BasePermission):
    def has_object_permission(self, request, view, timetable):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        if request.user == timetable.owner:
            return True
        return False


class TimetableProvider(BaseProvider):
    permission_classes = [Identity] # redundant but in case we make a mistake with the queryset
    model = Timetable

    @property
    def serializer_class(self):
        return MutateSerializer if self.request.mutate else ViewSerializer

    def get_queryset(self, request):
        return Timetable.objects.filter(
            owner=request.user,
            term__end_date__gte=timezone.now() - settings.TERM_GRACE_PERIOD,
        )

    def get_last_modified(self, view):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(
                    app_label="core", model="timetable"
                )
            )
            .filter(object_id=str(view.get_object().pk))
            .latest("action_time")
            .action_time
        )

    def get_last_modified_queryset(self):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="timetable")
            )
            .latest("action_time")
            .action_time
        )
