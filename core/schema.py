from functools import wraps
from typing import Optional, Sequence, Callable, Dict, Any, Type

from drf_spectacular.drainage import set_override
from drf_spectacular.utils import F, OpenApiExample
from rest_framework.serializers import Serializer


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

def split_api3_obj(endpoints):
    print(endpoints)
    # your modifications to the list of operations that are exposed in the schema
    for (path, path_regex, method, callback) in endpoints:
        pass
    return endpoints