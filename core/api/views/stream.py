import json
from queue import LifoQueue

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
        self.model = model
        self.signal = signal
        self.serializer = serializer
        self.q = LifoQueue()
        self.__setup()

    def __setup(self):
        self.signal.connect(self.__receive, sender=self.model)

    def __del__(self):
        self.signal.disconnect(self.__receive, sender=self.model)

    def __receive(self, instance, **_):
        self.q.put(instance)

    def __iter__(self):
        return self

    def __next__(self):
        instance = self.q.get()
        return f"data: {json.dumps(self.serializer(instance).data)}\n"
