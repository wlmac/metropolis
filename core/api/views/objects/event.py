import datetime

from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework import permissions, serializers
from rest_framework.exceptions import ParseError

from .announcement import Inner
from .base import BaseProvider
from .... import models
from ....models import Event

AOE = datetime.timezone(datetime.timedelta(hours=-12), name="AoE")


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
            "description",
            "tags",
        ]


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventProvider(BaseProvider):
    model = Event
    listing_filters_ignore = ["start", "end"]

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
        q = models.Event.objects.all()

        def parse(name):
            raw = self.request.query_params.get(name)
            if not raw:
                return None
            try:
                d = datetime.datetime.strptime(raw, "%Y-%m-%d")
                if name == "end":
                    # AoE time same day
                    d = d.replace(tzinfo=AOE, hour=23, minute=59, second=59)
                elif name == "start":
                    # AoE time prev day
                    d = d.replace(tzinfo=AOE)
                    d -= datetime.timedelta(days=1)
                return d
            except ValueError as e:
                raise ParseError(detail=f"parse {name}: {e}")

        start, end = parse("start"), parse("end")
        if start:
            q = q.filter(end_date__gte=start)
        if end:
            q = q.filter(start_date__lte=end)
        if start and end and start > end:
            raise ParseError("start is after end")
        if self.request.user.is_anonymous:
            q = q.filter(is_public=True)
        else:
            q = q.filter(
                Q(is_public=True) | Q(organization__member=self.request.user.id)
            )
        return q

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
