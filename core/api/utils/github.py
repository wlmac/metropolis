from functools import lru_cache
from os import environ
from typing import Iterable, Tuple, Optional, List, TYPE_CHECKING

from django.db import connection
from django.db.models import Model
from frozendict import frozendict

if TYPE_CHECKING:
    from frozendict import SelfT


def table_exists(model: Model) -> bool:
    """
    Check if the database table corresponding to the model exists.
    """
    # Check if the corresponding database table exists
    table_name = model._meta.db_table
    return table_name in connection.introspection.table_names()


def get_model_choices(
    model: Model,
    value_list: Tuple[str, str],
    db_filter: Optional["SelfT"] = None,
) -> List:
    db_filter = frozendict(db_filter) if db_filter else None

    @lru_cache(maxsize=None, typed=False)
    def _get_model_choices(
        model,
        value_list,
        db_filter,
    ):
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

    return _get_model_choices(model, value_list, db_filter)


def ci_safe(options: Iterable) -> Iterable:
    """
    Make options case-insensitive safe, returning an empty list in CI.
    """
    if environ.get("GITHUB_ACTIONS", False) is True:  # if running in CI
        return []
    else:
        return options
