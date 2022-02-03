import re

import bleach.sanitizer as sanitizer
from django import template
from django.contrib.sites.models import Site
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from martor.utils import markdownify

register = template.Library()

current_site = Site.objects.get_current()
bodge_pattern = re.compile(f"\[([^\]]*)\]\(/")


def bodge_replace(match):
    return f"[{match.group(1)}](https://{current_site.domain}/"


# https://github.com/mozilla/bleach/blob/main/bleach/sanitizer.py#L13

cleaner = sanitizer.Cleaner(
    tags=[
        *sanitizer.ALLOWED_TAGS,
        "br",
        "p",
        "img",
        *["h{}".format(i) for i in range(1, 7)],
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
        "iframe": ["src", "frameborder", "class"],
        "img": ["alt", "src"],
    },
    styles=["markdown-embed"],
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
