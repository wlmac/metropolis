import json
from queue import LifoQueue

from django.db.models import signals
from django.dispatch import Signal, receiver
from django.http import StreamingHttpResponse
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ... import models
from .. import serializers
from .stream import SignalStream

global_notifs = Signal()


@receiver(signals.post_save, sender=models.Announcement)
def announcement_change(sender, **kwargs):
    global_notifs.send("announcement_change", orig_sender=sender, kwargs=kwargs)


@receiver(signals.post_save, sender=models.BlogPost)
def blogpost_change(sender, **kwargs):
    global_notifs.send("blogpost_change", orig_sender=sender, kwargs=kwargs)


class NotificationStream:
    def __init__(
        self,
        signal,
        serializer,
    ):
        self.signal = signal
        self.serializer = serializer
        self.q = LifoQueue()
        self.__setup()

    def __setup(self):
        self.signal.connect(self.__receive)
        self.q.put(("init", {}))

    def __del__(self):
        self.signal.disconnect(self.__receive)

    def __receive(self, sender, **kwargs):
        self.q.put((sender, kwargs))

    def __iter__(self):
        return self

    def __next__(self):
        sender, kwargs = self.q.get()
        event_name, data = self.serializer(sender, **kwargs)
        return f"event: {event_name}\n" f"data: {json.dumps(data)}\n"


def serializer(sender, signal=None, orig_sender=None, kwargs={}):
    if sender == "announcement_change":
        return (
            sender,
            serializers.AnnouncementSerializer(kwargs["instance"]).data,
        )
    elif sender == "blogpost_change":
        return (
            sender,
            serializers.BlogPostSerializer(kwargs["instance"]).data,
        )
    else:
        return (sender, kwargs)


class NotificationsNew(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        response = StreamingHttpResponse(
            NotificationStream(
                signal=global_notifs,
                serializer=serializer,
            ),
            content_type="text/event-stream",
        )
        response["Cache-Control"] = "no-cache"
        return response
