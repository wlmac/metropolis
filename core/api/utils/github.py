from functools import lru_cache
from os import environ
from typing import Iterable, Tuple, Optional, Dict, List

from django.apps import apps
from django.db import connection
from django.db.models import Model


def table_exists(model: Model) -> bool:
	"""
	Check if the database table corresponding to the model exists.
	"""
	app_label = model._meta.app_label
	model_name = model.__name__
	
	# Check if the model is registered with Django
	if apps.get_model(app_label, model_name) is None:
		return False
	
	# Check if the corresponding database table exists
	table_name = model._meta.db_table
	return table_name in connection.introspection.table_names()


def get_model_choices(
		model: Model,
		value_list: Tuple[str, str],
		db_filter: Optional[Dict[str, str]] = None,
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
	
	# Convert the list of tuples into a tuple of tuples before sorting
	options = tuple(options)
	filter_key = tuple(sorted(options, key=lambda x: x[0])) if db_filter else None
	
	return ci_safe(options, model=model, filter_key=filter_key)


@lru_cache(maxsize=None, typed=False)
def ci_safe(
		options: Iterable, /, model: Model, filter_key: Optional[Tuple] = None
) -> Iterable:
	"""
	Make options case-insensitive safe, returning an empty list in CI.
	"""
	if (
			filter_key is not None and environ.get("GITHUB_ACTIONS", False) is True
	):  # if running in CI
		return []
	else:
		return options  # running in prod
