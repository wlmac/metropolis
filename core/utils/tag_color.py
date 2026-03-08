import colorsys

from django.conf import settings


def get_tag_color(hue: int) -> str:
    sat = settings.TAG_COLOR_SATURATION or 0.2
    val = settings.TAG_COLOR_VALUE or 1.0
    r, g, b = [int(i * 255) for i in colorsys.hsv_to_rgb(hue, sat, val)]
    return f"#{r:02x}{g:02x}{b:02x}"
