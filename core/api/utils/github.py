from os import environ
from typing import TYPE_CHECKING, Iterable, List, Optional, Tuple

from django.db import connection
from django.db.models import Model
from memoization import cached


def table_exists(model: Model) -> bool:
    """
    Check if the database table corresponding to the model exists.
    """
    # Check if the corresponding database table exists
    table_name = model._meta.db_table
    return table_name in connection.introspection.table_names()


@cached(max_size=512)
def get_model_choices(
    model: Model,
    value_list: Tuple[str, str],
    db_filter: Optional[dict] = None,
) -> List:
    """
    Get choices for a model with optional filtering.
    """
    if not table_exists(model):
        return []

    options: List
    if db_filter is None:
        options = list(model.objects.all().values_list(*value_list))
    else:
        options = list(model.objects.filter(**db_filter).values_list(*value_list))

    return ci_safe(options)


def ci_safe(options: Iterable) -> Iterable:
    """
    Make options case-insensitive safe, returning an empty list in CI.
    """
    if environ.get("GITHUB_ACTIONS", False) is True:  # if running in CI
        return []
    else:
        return options
