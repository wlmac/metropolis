import markdown

EMOJI_RE = r"(:[+\-\w]+:)"

REWRITES = {
    'tada': 'party popper'
}


class EmojiPattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        name = self.unescape(m.group(2)).replace('_', ' ')[1:-1]
        name = REWRITES.get(name, name)
        emoji = r'\N{' + name + r'}'
        converted = bytes(emoji, 'utf-8').decode('unicode_escape')
        return converted


class EmojiExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        """Setup `emoji_img` with EmojiPattern"""
        md.inlinePatterns["emoji_img"] = EmojiPattern(EMOJI_RE, md)


def makeExtension(*args, **kwargs):
    return EmojiExtension(*args, **kwargs)
