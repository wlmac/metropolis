import json

from django import forms
from django.conf import settings
from django.contrib.postgres.fields import (JSONField as DjangoJSONField, ArrayField as DjangoArrayField, )
from django.db.models import Field


class JSONField(DjangoJSONField):
	pass


class ArrayField(DjangoArrayField):
	def formfield(self, **kwargs):
		defaults = {'form_class': forms.MultipleChoiceField, 'choices': self.base_field.choices, }
		defaults.update(kwargs)
		# Skip our parent's formfield implementation completely as we don't
		# care for it.
		# pylint:disable=bad-super-call
		return super(ArrayField, self).formfield(**defaults)


if 'sqlite' in settings.DATABASES['default']['ENGINE']:
	class JSONField(Field):
		def db_type(self, connection):
			return 'text'
		
		def from_db_value(self, value, expression, connection):
			if value is not None:
				return self.to_python(value)
			return value
		
		def to_python(self, value):
			if value is not None:
				try:
					return json.loads(value)
				except (TypeError, ValueError):
					return value
			return value
		
		def get_prep_value(self, value):
			if value is not None:
				return str(json.dumps(value))
			return value
		
		def value_to_string(self, obj):
			return self.value_from_object(obj)
	
	
	class ArrayField(JSONField):
		def __init__(self, base_field, size=None, **kwargs):
			"""Care for DjangoArrayField's kwargs."""
			self.base_field = base_field
			self.size = size
			super().__init__(**kwargs)
		
		def deconstruct(self):
			"""Need to create migrations properly."""
			name, path, args, kwargs = super().deconstruct()
			kwargs.update({'base_field': self.base_field.clone(), 'size': self.size, })
			return name, path, args, kwargs
		
		def formfield(self, **kwargs):
			defaults = {'form_class': forms.MultipleChoiceField, 'choices': self.base_field.choices, }
			defaults.update(kwargs)
			# Skip our parent's formfield implementation completely as we don't
			# care for it.
			# pylint:disable=bad-super-call
			return super().formfield(**defaults)
