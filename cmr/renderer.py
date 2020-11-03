import shutil

from mistune import Renderer, escape, escape_link, markdown
from colors import color, strip_color
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

from cmr.tables import TableRenderer
from cmr.theme import DEFAULT_THEME


class TerminalRenderer(Renderer):
    def __init__(self, theme=DEFAULT_THEME, **kwargs):
        super().__init__(**kwargs)
        self._theme = theme
        self._columns, self._lines = shutil.get_terminal_size()
        self._table = None

    def header(self, text, level, raw=None):
        """Rendering header/heading tags like ``<h1>`` ``<h2>``.

        :param text: rendered text content for the header.
        :param level: a number for the header level, for example: 1.
        :param raw: raw text content of the header.
        """
        color_info = {}
        if self._theme is not None:
            color_info = self._theme.get('headings', {}).get(level, {})
        return color(
            f'{text}\n\n',
            **color_info,
        )

    def double_emphasis(self, text):
        """Rendering **strong** text.

        :param text: text content for emphasis.
        """
        color_info = {}
        if self._theme is not None:
            color_info = self._theme.get('strong', {})
        return color(text, **color_info)

    def emphasis(self, text):
        """Rendering *emphasis* text.

        :param text: text content for emphasis.
        """
        color_info = {}
        if self._theme is not None:
            color_info = self._theme.get('em', {})
        return color(text, **color_info)

    def strikethrough(self, text):
        """Rendering ~~strikethrough~~ text.

        :param text: text content for strikethrough.
        """
        color_info = {}
        if self._theme is not None:
            color_info = self._theme.get('del', {})
        text = self._strike(text)
        return color(f'{text}', **color_info)

    def list(self, body, ordered=True):
        """Rendering list tags like ``<ul>`` and ``<ol>``.

        :param body: body contents of the list.
        :param ordered: whether this list is ordered or not.
        """
        color_info = {}
        sep = '. ' if ordered else '  '
        symbol = '*'
        if self._theme is not None:
            theme_info = self._theme.get('ol' if ordered else 'ul', {})
            sep = theme_info.get('separator', sep)
            color_info = theme_info.get('color', {})
            symbol = theme_info.get('symbol', symbol)
        if ordered:
            sep = '. '

            return (
                '\n'.join(
                    [
                        color(f'  {idx}{sep}{text}', **color_info)
                        for idx, text in enumerate(body.splitlines(), start=1)
                    ]
                )
                + '\n\n'
            )
        return (
            '\n'.join(
                [
                    color(f'  {symbol}{sep}{text}', **color_info)
                    for text in body.splitlines()
                ]
            )
            + '\n\n'
        )

    def list_item(self, text):
        """Rendering list item snippet. Like ``<li>``."""
        return '%s\n' % text

    def block_code(self, code, lang=None):
        """Rendering block level code. ``pre > code``.

        :param code: text content of the code block.
        :param lang: language of the given code.
        """
        lexer = get_lexer_by_name(lang) if lang else guess_lexer(code)
        hl = highlight(code, lexer, TerminalFormatter(bg='dark', linenos=False))
        return f'\n{hl}\n'

    def block_quote(self, text):
        """Rendering <blockquote> with the given text.

        :param text: text content of the blockquote.
        """
        color_info = {}
        symbol = '|'
        sep = ' '
        indent = '  '
        if self._theme is not None:
            theme_info = self._theme.get('blockquote', {})
            color_info = theme_info.get('color', {})
            symbol = theme_info.get('symbol', symbol)
            sep = theme_info.get('separator', sep)
            indent = theme_info.get('indent', indent)

        lines = text.splitlines()
        lines = [
            color(f'{indent}{symbol}{sep}{strip_color(line)}', **color_info) for line in lines
        ]
        return '\n\n' + '\n'.join(lines[:-1]) + '\n\n'

    def hrule(self):
        color_info = {}
        delimiter = '*'
        line = '-' * (self._columns - 2)
        if self._theme is not None:
            theme_info = self._theme.get('hr', {})
            delimiter = theme_info.get('delimiter', delimiter)
            line = theme_info.get('line', '-') * (self._columns - 2)
            color_info = theme_info.get('color', {})
        return color(
            f'\n{delimiter}{line}{delimiter}\n\n',
            **color_info,
        )

    def paragraph(self, text):
        """Rendering paragraph tags. Like ``<p>``."""
        color_info = {}
        if self._theme is not None:
            color_info = self._theme.get('p', {})
        text = text.strip(' ')
        return color(f'{text}', **color_info) + '\n\n'

    def codespan(self, text):
        """Rendering inline `code` text.

        :param text: text content for inline code.
        """

        color_info = {}
        if self._theme is not None:
            color_info = self._theme.get('code', {})

        text = escape(text.rstrip(), smart_amp=False)
        return color(text, **color_info)

    def linebreak(self):
        """Rendering line break like ``<br>``."""
        return '\n'

    def text(self, text):
        """Rendering unformatted text.

        :param text: text content.
        """
        return escape(text)

    def block_html(self, html):
        """Rendering block level pure html content.

        :param html: text content of the html snippet.
        """
        return ''

    def table(self, header, body):
        """Rendering table element. Wrap header and body in it.

        :param header: header part of the table.
        :param body: body part of the table.
        """
        rendered = ''
        if self._table:
            rendered = self._table.render()
            self._table = None
        return rendered

    def table_row(self, content):
        if self._table:
            self._table.new_row()
        return ''

    def table_cell(self, content, **flags):
        """Rendering a table cell. Like ``<th>`` ``<td>``.

        :param content: content of current table cell.
        :param header: whether this is header or not.
        :param align: align of current table cell.
        """
        header = flags['header']
        align = flags['align']

        theme = self._theme.get('table', {})
        if not self._table:
            self._table = TableRenderer(
                **theme
            )

        if header:
            self._table.add_header_cell(content, align)
        else:
            self._table.add_cell(content)
        return ''

    def escape(self, text):
        """Rendering escape sequence.

        :param text: text content.
        """
        return escape(text)

    def _render_link(self, link, title, text, theme_tag):
        link = escape_link(link)
        link_color = {}
        text_color = {}
        start = '->'
        end = '<-'

        if self._theme is not None:
            theme_info = self._theme.get(theme_tag, {})
            start = theme_info.get('start_symbol', start)
            end = theme_info.get('end_symbol', end)
            text_color = theme_info.get('text_color', text_color)
            link_color = theme_info.get('link_color', link_color)
        text = color(text, **text_color)
        link = color(f' {start} {link} {end}', **link_color)
        return f'{text}{link}'

    def autolink(self, link, is_email=False):
        return self.link(link, '', link)

    def link(self, link, title, text):
        """Rendering a given link with content and title.

        :param link: href link for ``<a>`` tag.
        :param title: title content for `title` attribute.
        :param text: text content for description.
        """
        return self._render_link(link, title, text, 'a')

    def image(self, src, title, text):
        """Rendering a image with title and text.

        :param src: source link of the image.
        :param title: title text of the image.
        :param text: alt text of the image.
        """
        return self._render_link(src, title, text, 'img')

    def inline_html(self, html):
        """Rendering span level pure html content.

        :param html: text content of the html snippet.
        """
        return ''

    def newline(self):
        """Rendering newline element."""
        return '\n'

    def footnote_ref(self, key, index):
        """Rendering the ref anchor of a footnote.

        :param key: identity key for the footnote.
        :param index: the index count of current footnote.
        """
        return ''

    def footnote_item(self, key, text):
        """Rendering a footnote item.

        :param key: identity key for the footnote.
        :param text: text content of the footnote.
        """
        return ''

    def footnotes(self, text):
        """Wrapper for all footnotes.

        :param text: contents of all footnotes.
        """
        return ''

    def _strike(self, text):
        result = ''
        for c in text:
            result = result + c + '\u0336'
        return result


def render(md, theme=DEFAULT_THEME):
    renderer = TerminalRenderer(theme=theme)
    return markdown(md, renderer=renderer)
