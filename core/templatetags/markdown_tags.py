import bleach.sanitizer as sanitizer
from django import template
from django.utils.safestring import mark_safe
from martor.utils import markdownify

register = template.Library()

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
    ],
    attributes={
        **sanitizer.ALLOWED_ATTRIBUTES,
        "iframe": ["src", "frameborder", "class"],
        "img": ["alt", "src"],
    },
    styles=["markdown-embed"],
    protocols=[
        "https",
        "mailto",
    ],
    strip=True,
)


@register.filter
def markdown(field_name):
    return mark_safe(cleaner.clean(markdownify(field_name)))
