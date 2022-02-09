import re

import bleach.sanitizer as sanitizer
import mistune
from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, lang=None):
        if lang:
            formatter = html.HtmlFormatter()
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except ClassNotFound:
                pass
            else:
                return highlight(code, lexer, formatter)
        return "<pre><code>" + mistune.escape(code) + "</code></pre>"


render = mistune.create_markdown(renderer=HighlightRenderer(escape=False))

register = template.Library()

bodge_pattern = re.compile(f"\[([^\]]*)\]\(/")


def bodge_replace(match):
    return f"[{match.group(1)}]({settings.ROOT}/"


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
        "iframe": ["src", "frameborder", "class", "title", "allow", "allowfullscreen", "width", "height"],
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
        cleaner.clean(render(re.sub(bodge_pattern, bodge_replace, field_name)))
    )
