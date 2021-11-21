import json
import time
from queue import Empty, LifoQueue

from django.db.models import signals

from ... import models
from .. import serializers


class SignalStream:
    def __init__(
        self,
        model,
        signal,
        serializer,
    ):
        self.__model = model
        self.__signal = signal
        self.__serializer = serializer
        self.__q = LifoQueue()
        self.__setup()

    def __setup(self):
        self.__signal.connect(self.__receive, sender=self.__model)

    def __del__(self):
        self.__signal.disconnect(self.__receive, sender=self.__model)

    def __receive(self, instance, **_):
        self.__q.put(instance)

    def __iter__(self):
        return self

    def __next__(self):
        instance = self.__q.get()
        return json.dumps(self.__serializer(instance).data) + "\n"
