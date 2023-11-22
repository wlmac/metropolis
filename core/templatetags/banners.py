import typing

from django import template
from core.api.views import Banners

register = template.Library()


@register.simple_tag
def banners(banner_type: typing.Literal["current", "upcoming", "all"]):
    if banner_type != "all":
        return Banners.calculate_banners()[banner_type]
    return Banners.calculate_banners()
