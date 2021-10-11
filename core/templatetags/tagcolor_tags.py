from django import template

from ..utils.tag_color import get_tag_color

register = template.Library()


@register.simple_tag
def tag_color(hue):
    return get_tag_color(hue)
