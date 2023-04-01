from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions, serializers

from .announcement import Inner
from .base import BaseProvider
from .... import models
from ....models import Event


class SuperficialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "organization",
            "should_announce",
        ]


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventProvider(BaseProvider):
    model = Event

    @property
    def serializer_class(self):
        return DetailSerializer if self.request.detail else SuperficialSerializer

    @property
    def permission_classes(self):
        return (
            [permissions.DjangoModelPermissions, Inner]
            if self.request.mutate
            else [permissions.AllowAny]
        )

    def get_queryset(self, request):
        start = timezone.now()
        if self.request.data.get("start"):
            start = self.request.data.get("start")
        elif self.request.query_params.get("start"):
            start = self.request.query_params.get("start")

        if not self.request.user.is_anonymous:
            if self.request.data.get("end"):
                end = self.request.data.get("end")
                events = (
                    models.Event.objects.filter(
                        end_date__gte=start, start_date__lte=end
                    )
                    .filter(
                        Q(is_public=True) | Q(organization__member=self.request.user.id)
                    )
                    .distinct()
                    .order_by("start_date")
                )
            elif self.request.query_params.get("end"):
                end = self.request.query_params.get("end")
                events = (
                    models.Event.objects.filter(
                        end_date__gte=start, start_date__lte=end
                    )
                    .filter(
                        Q(is_public=True) | Q(organization__member=self.request.user.id)
                    )
                    .distinct()
                    .order_by("start_date")
                )
            else:
                events = (
                    models.Event.objects.filter(end_date__gte=start)
                    .filter(
                        Q(is_public=True) | Q(organization__member=self.request.user.id)
                    )
                    .distinct()
                    .order_by("start_date")
                )
        else:
            if self.request.data.get("end"):
                end = self.request.data.get("end")
                events = models.Event.objects.filter(
                    end_date__gte=start, start_date__lte=end, is_public=True
                ).order_by("start_date")
            elif self.request.query_params.get("end"):
                end = self.request.query_params.get("end")
                events = models.Event.objects.filter(
                    end_date__gte=start, start_date__lte=end, is_public=True
                ).order_by("start_date")
            else:
                events = models.Event.objects.filter(
                    end_date__gte=start, is_public=True
                ).order_by("start_date")

        return events

    def get_last_modified(self, view):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="event")
            )
            .filter(object_id=str(view.get_object().pk))
            .latest("action_time")
            .action_time
        )

    def get_last_modified_queryset(self):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="event")
            )
            .latest("action_time")
            .action_time
        )
