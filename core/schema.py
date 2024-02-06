import dataclasses
from dataclasses import dataclass, Field
from functools import wraps
from typing import (
    Optional,
    Sequence,
    Callable,
    Dict,
    Any,
    Type,
    Tuple,
    List,
    NamedTuple,
)

from drf_spectacular.drainage import set_override
from drf_spectacular.utils import F, OpenApiExample
from rest_framework.serializers import Serializer

from logging import getLogger

from core.api.utils.polymorphism import get_provider, get_providers_by_operation
from core.api.v3.objects import BaseProvider
from core.utils.types import APIObjOperations, PathData

logger = getLogger(__name__)


def metro_extend_schema_serializer(  # modified version of drf_spectacular.utils.extend_schema_serializer
    klass: Type[Serializer],
    many: Optional[bool] = None,
    exclude_fields: Optional[Sequence[str]] = None,
    deprecate_fields: Optional[Sequence[str]] = None,
    examples: Optional[Sequence[OpenApiExample]] = None,
    extensions: Optional[Dict[str, Any]] = None,
    component_name: Optional[str] = None,
) -> Callable[[F], F]:
    """
    Function for modifying the behavior of a serializer class. Intended for overriding default serializer
    behavior that can't be influenced through: func:`~drf_spectacular.utils.extend_schema`.

    :param klass: The serializer class to modify.
    :param many: Override how the serializer is initialized. Mainly used to coerce the list view detection
        heuristic to acknowledge a non-list serializer.
    :param exclude_fields: Fields to ignore while processing the serializer. Only affects the
        schema. Fields will still be exposed through the API.
    :param deprecate_fields: Fields to mark as deprecated while processing the serializer.
    :param examples: Define example data for the serializer.
    :param extensions: Specification extensions, e.g., ``x-is-dynamic``, etc.
    :param component_name: Override the default class name extraction.
    """
    if many is not None:
        set_override(klass, "many", many)
    if exclude_fields:
        set_override(klass, "exclude_fields", exclude_fields)
    if deprecate_fields:
        set_override(klass, "deprecate_fields", deprecate_fields)
    if examples:
        set_override(klass, "examples", examples)
    if extensions:
        set_override(klass, "extensions", extensions)
    if component_name:
        set_override(klass, "component_name", component_name)

    return klass


def dynamic_envelope(serializer_class: Type[Serializer], many=False):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            component_name = (
                f'Enveloped{serializer_class.__name__.replace("Serializer", "")}'
            )
            component_name += "List" if many else ""

            metro_extend_schema_serializer(
                serializer_class, many=False, component_name=component_name
            )

            response = view_func(*args, **kwargs)

            return response

        return wrapped_view

    return decorator


def run_fixers(result, generator, request, public):
    fixer = Api3ObjSpliter(result)
    fixer.run()
    return fixer.schema


@dataclass
class SingleOperationData:
    providers: List[BaseProvider]
    operation: APIObjOperations
    data: dict
@dataclass
class ObjectModificationData:
    retrieve: Optional[SingleOperationData] = None
    single: Optional[SingleOperationData] = None
    list: Optional[SingleOperationData] = None
    new: Optional[SingleOperationData] = None
    
    def __iter__(self):
        return iter(
            [
                ("retrieve", self.retrieve),
                ("single", self.single),
                ("list", self.list),
                ("new", self.new),
            ]
        )

class Api3ObjSpliter:
    """
    Split the API3 schema into the different paths based on the object type and provider
    """

    defaults = {
        "tags": ["Objects", "V3"],
    }

    def __init__(self, schema):
        self.operation_data: ObjectModificationData = ObjectModificationData()
        self.keys_to_delete: Tuple = ()
        self.schema = schema

    def run(self):
        # ObjectModificationData._make
        paths = self.schema["paths"]
        self.set_obj_paths(paths)
        
        for operation in dataclasses.fields(self.operation_data):
            self.create_obj_views(operation)

        self.del_obj_paths()

    def del_obj_paths(self) -> None:
        for path in self.keys_to_delete:
            del self.schema["paths"][path]

    def set_obj_paths(self, paths: Dict[str, dict]) -> List[Tuple[str, dict]]:
        PATH_PREFIX = "/api/v3/obj/{type}"
        _obj_paths = [
            (path, value)
            for path, value in paths.items()
            if path.startswith(PATH_PREFIX)
        ]
        self.keys_to_delete = tuple([path for path, _ in _obj_paths])
        get_name = lambda id: id.split("_")[-1]
        for _, value in _obj_paths:
            http_method = list(value.keys())[0]
            operation_id = value[http_method]["operationId"]
            name = get_name(operation_id)
            # set values for ObjectModificationData
            insertable_value = SingleOperationData(
                operation=http_method,
                data=value[http_method],
                providers=get_providers_by_operation(http_method, return_provider=True),
            )
            setattr(self.operation_data, name, insertable_value)
        if not self.operation_data:
            raise ValueError("No paths found, API3 obj docs will be broken.")

    def get_providers_from_name(self, enum: List[str]) -> List[BaseProvider]:
        return [get_provider(key) for key in enum]

    def create_obj_views(self, operation: SingleOperationData):
        ...
