import json

from django.db.models import signals
from django.http import StreamingHttpResponse
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ... import models
from .. import serializers
from .stream import SignalStream


class AnnouncementListAll(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.AnnouncementSerializer

    def get_queryset(self):
        return models.Announcement.get_all(user=self.request.user)


class AnnouncementListMyFeed(APIView):
    permission_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["me_ann"]
    serializer_class = serializers.AnnouncementSerializer

    def get_queryset(self):
        return self.request.user.get_feed()


class AnnouncementStream(SignalStream):
    def __next__(self):
        instance = self.q.get()
        if instance.status != "a":
            # because Announcement is not approved, don't send
            return self.__next__()
        return (
            f"event: announcement-changes\n"
            f"data: {json.dumps(self.serializer(instance).data)}\n"
        )


class AnnouncementChangeStream(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        response = StreamingHttpResponse(
            AnnouncementStream(
                signal=signals.post_save,
                model=models.Announcement,
                serializer=serializers.AnnouncementSerializer,
                event_name="announcement_change",
            ),
            content_type="text/event-stream",
        )
        response["Cache-Control"] = "no-cache"
        return response
