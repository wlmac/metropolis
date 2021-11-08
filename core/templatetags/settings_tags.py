from django import template
from django.conf import settings
from django.shortcuts import reverse
from django.utils.safestring import mark_safe

from .. import models

register = template.Library()


@register.simple_tag
def settings_value(name):
    return getattr(settings, name)
