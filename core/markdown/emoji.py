import markdown

EMOJI_RE = r"(:[+\-\w]+:)"

REWRITES = {
    "checkered flag": "chequered flag",
    "grey question": "question mark",
    "white check mark": "check mark",
    "question": "question mark",
    "tada": "party popper",
}


class EmojiPattern(markdown.inlinepatterns.Pattern):
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


class EmojiExtension(markdown.Extension):
    def extendMarkdown(self, md):
        """Setup `emoji_img` with EmojiPattern"""
        md.inlinePatterns.register("emoji_img", EmojiPattern(EMOJI_RE, md))


def makeExtension(*args, **kwargs):
    return EmojiExtension(*args, **kwargs)
