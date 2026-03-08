import hashlib
import urllib

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# return only the URL of the gravatar
# TEMPLATE USE:  {{ email|gravatar_url:150 }}
@register.filter
def gravatar_url(email, size=40):
    email_hash = hashlib.md5(email.encode("utf-8").lower()).hexdigest()
    query_string = urllib.parse.urlencode({"d": "retro", "s": str(size)})
    return f"https://www.gravatar.com/avatar/{email_hash}?{query_string}"


# return an image tag with the gravatar
# TEMPLATE USE:  {{ email|gravatar:150 }}
@register.filter
def gravatar(email, size=40):
    url = gravatar_url(email, size)
    return mark_safe(f'<img src="{url}" width="{size}" height="{size}">')
