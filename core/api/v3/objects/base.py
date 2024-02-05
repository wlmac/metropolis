from typing import List, Literal, Dict, Final
from rest_framework.serializers import BaseSerializer
from abc import ABC
from django.db.models import Model, QuerySet

type SerializerItems = Dict[str, BaseSerializer]

class BaseProvider(ABC):
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
    
    @classmethod
    def _run_typechecking(cls):
        get_attrs: Final[str] = ("queryset", )
        required_attrs: Final[Dict[str, type]] = {"model": Model, "raw_serializers": dict}
        additional_attrs: Final[Dict[str,type]] = {"additional_lookup_fields": QuerySet}
        
        for key in get_attrs:
            if not (hasattr(cls, key) or hasattr(cls, f'get_{key}')): # todo check if callable
                raise AttributeError(f'{cls} must either define {key} or :meth:get_{key}') 
            
        for key, type in required_attrs:
            if not hasattr(cls, key):
                raise AttributeError(f'{cls} must define attr {key} of type {type}')
            
        # just type checking, doesnt care if value is there or not.    
        for key, value in (additional_attrs + required_attrs).items():
            if item := getattr(cls, key):
              if not type(item, value):
                  raise TypeError(f'{key} must be of type {value}')  
        
        cls._check_serializers()
        
    @classmethod
    def _check_serializers(cls):
        for key in cls.raw_serializers:
            if key not in ("list", "new", "single", "retrieve", "_"):
                raise AttributeError(f"key {key} is not a valid key for raw_serializers")

    def __new__(cls, request):
        from core.api.utils.polymorphism import serializer_fmt as SFMT # noqa
        cls._run_typechecking()
        
        instance = super().__new__(cls)
        instance.serializers = SFMT(cls.raw_serializers)
        return instance
        
    def __init__(self, request):
        self.request = request
        

