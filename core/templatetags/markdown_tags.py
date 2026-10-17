import re
from urllib.parse import urlsplit

import bleach.sanitizer as sanitizer
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from martor.utils import markdownify

register = template.Library()

bodge_pattern = re.compile(r"\[([^]]*)]\(/")


def bodge_replace(match):
    return f"[{match.group(1)}]({settings.ROOT}/"


# hosts already embedded on the site; add one here to allow a new embed source
IFRAME_HOSTS = {
    "open.spotify.com",
    "w.soundcloud.com",
    "www.youtube.com",
    "www.youtube-nocookie.com",
}
IFRAME_ATTRS = {
    "frameborder",
    "class",
    "title",
    "allow",
    "allowfullscreen",
    "width",
    "height",
}


def iframe_attr(tag, name, value):
    if name == "src":
        return urlsplit(value).hostname in IFRAME_HOSTS
    return name in IFRAME_ATTRS


# https://github.com/mozilla/bleach/blob/main/bleach/sanitizer.py#L13

cleaner = sanitizer.Cleaner(
    tags=[
        *sanitizer.ALLOWED_TAGS,
        "br",
        "p",
        "img",
        *[f"h{i}" for i in range(1, 7)],
        "hr",
        "iframe",
        "ol",
        "ul",
        "li",
        "strong",
        "em",
        "blockquote",
        "pre",
        "code",
    ],
    attributes={
        **sanitizer.ALLOWED_ATTRIBUTES,
        "iframe": iframe_attr,
        "img": ["alt", "src"],
    },
    protocols=[
        "http",
        "https",
        "mailto",
    ],
    strip=True,
)


@register.filter
@stringfilter
def markdown(field_name):
    return mark_safe(
        cleaner.clean(markdownify(re.sub(bodge_pattern, bodge_replace, field_name)))
    )
