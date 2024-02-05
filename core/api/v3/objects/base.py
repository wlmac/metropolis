from typing import List, Literal, Dict
from rest_framework.serializers import BaseSerializer

type SerializerItems = Dict[str, BaseSerializer]

class BaseProvider:
    allow_list: bool = (
        True  # Is the view able to list the model's objects. (e.g. /user would list all users
    )
    allow_new: bool = True  # Is the provider able to create a new object.
    kind: Literal["list", "new", "single", "retrieve"]  # type of view
    listing_filters_ignore: List[str] = []
    raw_serializers: SerializerItems
    
    @property
    def serializer_class(self):
        return self.serializers.get(self.request.kind)
    
    def __new__(cls, request):
        from core.api.utils.polymorphism import serializer_fmt as SFMT # noqa
        instance = super().__new__(cls)
        instance.serializers = SFMT(cls.raw_serializers)
        return instance
        
    def __init__(self, request):
        self.request = request

