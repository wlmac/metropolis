from django import template
from django.utils.safestring import mark_safe
from django.shortcuts import reverse
from .. import models
import courseshare.settings as settings
 
register = template.Library()
 
@register.simple_tag
def settings_value(name):
    return getattr(settings, name)
