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


list_marker = re.compile(r"(\d+\.|[*+-]) ")


def split_adjacent_lists(text):
    """Python-Markdown merges a numbered list and a bulleted list that follow each other
    into one list; an invisible paragraph between them keeps them apart.
    shortcut: also applies inside fenced code blocks, fine until someone writes list-like code."""
    out, last = [], None
    for line in text.split("\n"):
        m = list_marker.match(line)
        if m:
            kind = "ol" if m.group(1)[0].isdigit() else "ul"
            if last and last != kind:
                if out and out[-1].strip():
                    out.append("")
                out += ["\u200b", ""]
            last = kind
        elif line.strip() and not line[0].isspace():
            last = None
        out.append(line)
    return "\n".join(out)


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
        # the "tables" markdown extension is on; no attributes allowed, so these stay inert
        "table",
        "thead",
        "tbody",
        "tr",
        "th",
        "td",
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
        cleaner.clean(
            markdownify(
                split_adjacent_lists(re.sub(bodge_pattern, bodge_replace, field_name))
            )
        )
    )
