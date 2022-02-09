from django import template
from django.shortcuts import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from ..utils.tag_color import get_tag_color

from .. import models

register = template.Library()

def pubreq_status(status: str):
    return format_html(
        '<span role="status" class="tag" style="background-color: {0};">{1}</span>',
        models.choices.PUBREQ_COLOURS[status],
        models.choices.PUBREQ_STATUS_NAMES[status]
    )

PUBREQ_IN_REQUESTERS = format_html(
    '<span class="tag" style="background-color: {0};">Requested</span>',
    get_tag_color(0.6),
)

PUBREQ_IN_APPROVERS = format_html(
    '<span class="tag" style="background-color: {0};">Approvable</span>',
    get_tag_color(0.7),
)

@register.filter
def pubreq_tags(pubreq_obj, user=None):
    return mark_safe(''.join([
        pubreq_status(pubreq_obj.status),
        PUBREQ_IN_REQUESTERS if user in pubreq_obj.requesters.all() else '',
        PUBREQ_IN_APPROVERS if user in pubreq_obj.approvers.all() else '',
    ]))
