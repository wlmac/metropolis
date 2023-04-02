from django.utils.text import capfirst
from multiselectfield import MultiSelectField, MultiSelectFormField


class CustomMultiSelectFormField(MultiSelectFormField):
    def check(self):
        ...


class CustomMultiSelectField(MultiSelectField):
    def formfield(self, **kwargs):
        defaults = {
            "required": not self.blank,
            "label": capfirst(self.verbose_name),
            "help_text": self.help_text,
            "choices": self.choices,
            "max_length": self.max_length,
            "max_choices": self.max_choices,
        }
        if self.has_default():
            defaults["initial"] = self.get_default()
        defaults.update(kwargs)
        return CustomMultiSelectField(**defaults)
