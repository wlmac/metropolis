import typing

from django import template
from core.api.views import Banners

register = template.Library()


@register.simple_tag
def banners(filter: typing.Literal["current", "upcoming", "all"]):
    print(Banners.calculate_banners())
    print("^")
    if filter != "all":
        return Banners.calculate_banners()[filter]
    return Banners.calculate_banners()
