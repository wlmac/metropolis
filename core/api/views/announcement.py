import json

from django.db.models import Q, signals
from django.http import StreamingHttpResponse
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ... import models
from .. import serializers
from .stream import SignalStream


class AnnouncementListAll(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        announcements = models.Announcement.get_all(user=request.user)
        serializer = serializers.AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)


class AnnouncementListMyFeed(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ["me_ann"]

    def get(self, request, format=None):
        announcements = request.user.get_feed()
        serializer = serializers.AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)


class AnnouncementStream(SignalStream):
    def __next__(self):
        instance = self.q.get()
        if instance.status != "a":
            # because Announcement is not approved, don't send
            return self.__next__()
        return f"data: {json.dumps(self.serializer(instance).data)}\n"


class AnnouncementChangeStream(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        response = StreamingHttpResponse(
            AnnouncementStream(
                signal=signals.post_save,
                model=models.Announcement,
                serializer=serializers.AnnouncementSerializer,
            ),
            content_type="text/event-stream",
        )
        response["Cache-Control"] = "no-cache"
        return response
