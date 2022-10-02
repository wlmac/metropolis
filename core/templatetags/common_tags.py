from django import template

register = template.Library()


@register.filter
def startswith(string, substring):
    return string.startswith(substring)


@register.filter
def split(string, split_char=" "):
    return string.split(split_char)


@register.filter
def gettype(obj):
    return obj.__class__.__name__


@register.simple_tag
def joinstr(*args):
    return "".join(map(str, args))
