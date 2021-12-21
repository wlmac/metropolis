import bleach.sanitizer as sanitizer
from django import template
from django.utils.safestring import mark_safe
from martor.utils import markdownify

register = template.Library()

cleaner = sanitizer.Cleaner(
    tags=[*sanitizer.ALLOWED_TAGS, "p"],
)


@register.filter
def markdown(field_name):
    print(markdownify(field_name))
    print(cleaner.clean(markdownify(field_name)))
    return mark_safe(cleaner.clean(markdownify(field_name)))
