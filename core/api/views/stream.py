import json
from queue import LifoQueue


class SignalStream:
    def __init__(
        self,
        model,
        signal,
        serializer,
        event_name,
    ):
        self.model = model
        self.signal = signal
        self.serializer = serializer
        self.q = LifoQueue()
        self.event_name = event_name
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
        return (
            f"event: {self.event_name}\n"
            f"data: {json.dumps(self.serializer(instance).data)}\n"
        )
