from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

EMOJI_RE = r"(:[+\-\w]+:)"

REWRITES = {
    "checkered flag": "chequered flag",
    "grey question": "question mark",
    "white check mark": "check mark",
    "question": "question mark",
    "tada": "party popper",
}


class EmojiPattern(Pattern):
    def handleMatch(self, m):
        orig = self.unescape(m.group(2))
        name = orig.replace("_", " ")[1:-1]
        name = REWRITES.get(name, name)
        emoji = r"\N{" + name + r"}"
        try:
            converted = bytes(emoji, "utf-8").decode("unicode_escape")
        except UnicodeDecodeError:
            return orig
        else:
            return converted


class EmojiExtension(Extension):
    def extendMarkdown(self, md):
        """Setup `emoji_img` with EmojiPattern"""
        md.inlinePatterns.register(EmojiPattern(EMOJI_RE, md), "emoji_img", 123 * 2)


def makeExtension(*args, **kwargs):
    return EmojiExtension(**kwargs)
