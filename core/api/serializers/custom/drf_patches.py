from django.utils.translation import gettext_lazy as _
from rest_framework.fields import ChoiceField, empty
from rest_framework.utils import html


class KwargChoiceField(ChoiceField):
	def __init__(self, **kwargs):
		self.choices = kwargs.pop('choices')
		self.html_cutoff = kwargs.pop('html_cutoff', self.html_cutoff)
		self.html_cutoff_text = kwargs.pop('html_cutoff_text', self.html_cutoff_text)
		
		self.allow_blank = kwargs.pop('allow_blank', False)
		
		super(ChoiceField, self).__init__(**kwargs)


class KwargMultipleChoiceField(KwargChoiceField): # a copy of MultipleChoiceField from drf source code with a different base class
	default_error_messages = {
		'invalid_choice': _('"{input}" is not a valid choice.'),
		'not_a_list': _('Expected a list of items but got type "{input_type}".'),
		'empty': _('This selection may not be empty.')
	}
	default_empty_html = []
	
	
	def __init__(self, **kwargs):
		self.allow_empty = kwargs.pop('allow_empty', True)
		super().__init__(**kwargs)
	
	def get_value(self, dictionary):
		if self.field_name not in dictionary:
			if getattr(self.root, 'partial', False):
				return empty
		# We override the default field access in order to support
		# lists in HTML forms.
		if html.is_html_input(dictionary):
			return dictionary.getlist(self.field_name)
		return dictionary.get(self.field_name, empty)
	
	def to_internal_value(self, data):
		if isinstance(data, str) or not hasattr(data, '__iter__'):
			self.fail('not_a_list', input_type=type(data).__name__)
		if not self.allow_empty and len(data) == 0:
			self.fail('empty')
		
		return {
			# Arguments for super() are needed because of scoping inside
			# comprehensions.
			super(self).to_internal_value(item)
			for item in data
		}
	
	def to_representation(self, value):
		return {
			self.choice_strings_to_values.get(str(item), item) for item in value
		}



