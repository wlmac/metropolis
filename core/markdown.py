# from markdown.util.etree import Element
import markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

EMBED_RE = r"\{(https?://.+)\}"


class EmbedPattern(Pattern):
    def handleMatch(self, m):
        el = markdown.util.etree.Element("iframe")
        el.set("src", m.group(2))
        el.set("class", "markdown-embed")
        el.set("frameborder", "0")
        return el


class EmbedExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(EmbedPattern(EMBED_RE, md), "embed", 123)


def makeExtension(*args, **kwargs):
    return EmbedExtension(*args, **kwargs)
