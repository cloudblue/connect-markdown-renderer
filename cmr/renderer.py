import re
import shutil

from mistune import Renderer, escape, escape_link, markdown
from colors import color
from prettytable import PrettyTable
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

from cmr.theme import DEFAULT_THEME


class TerminalRenderer(Renderer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._theme = kwargs.get('theme', DEFAULT_THEME)
        self._columns, self._lines = shutil.get_terminal_size()
        self._table_rows = None
        self._table_row = None

    def strike(self, text):
        result = ''
        for c in text:
            result = result + c + '\u0336'
        return result

    def header(self, text, level, raw=None):
        """Rendering header/heading tags like ``<h1>`` ``<h2>``.

        :param text: rendered text content for the header.
        :param level: a number for the header level, for example: 1.
        :param raw: raw text content of the header.
        """
        theme = self._theme['headings'][level]
        # indent = ' ' * (level - 1)
        indent = ''
        return color(
            f'{indent}{text}\n\n',
            **theme,
        )

    def double_emphasis(self, text):
        """Rendering **strong** text.

        :param text: text content for emphasis.
        """
        theme = self._theme['strong']
        return color(text, **theme)

    def emphasis(self, text):
        """Rendering *emphasis* text.

        :param text: text content for emphasis.
        """
        theme = self._theme['em']
        return color(text, **theme)

    def strikethrough(self, text):
        """Rendering ~~strikethrough~~ text.

        :param text: text content for strikethrough.
        """
        theme = self._theme['strikethrough']
        text = self.strike(text)
        return color(f'{text}', **theme)

    def list(self, body, ordered=True):
        """Rendering list tags like ``<ul>`` and ``<ol>``.

        :param body: body contents of the list.
        :param ordered: whether this list is ordered or not.
        """
        if ordered:
            theme = self._theme['ol']
            sep = theme['separator']
            return '\n' + '\n'.join([
                color(f'  {idx}{sep}{text}', **theme['color'])
                for idx, text in enumerate(body.splitlines(), start=1)
            ]) + '\n\n'
        theme = self._theme['ul']
        symbol = theme['symbol']
        sep = theme['separator']
        return '\n' + '\n'.join([
            color(f'  {symbol}{sep}{text}', **theme['color'])
            for text in body.splitlines()
        ]) + '\n\n'

    def list_item(self, text):
        """Rendering list item snippet. Like ``<li>``."""
        return '%s\n' % text

    def block_code(self, code, lang=None):
        """Rendering block level code. ``pre > code``.

        :param code: text content of the code block.
        :param lang: language of the given code.
        """
        lexer = get_lexer_by_name(lang) if lang else guess_lexer(code)
        hl = highlight(code, lexer, TerminalFormatter(bg='dark', linenos=True))
        return f'\n{hl}\n'

    def block_quote(self, text):
        """Rendering <blockquote> with the given text.

        :param text: text content of the blockquote.
        """
        theme = self._theme['blockquote']
        symbol = theme['symbol']
        sep = theme['separator']
        indent = theme['indent']
        lines = text.splitlines()
        lines = [
            color(f'{indent}{symbol}{sep}{line}', **theme['color'])
            for line in lines
        ]
        return '\n'.join(lines) + '\n'

    def hrule(self):
        theme = self._theme['hr']
        delimiter = theme['delimiter']
        line = theme['line'] * (self._columns - 2)
        return color(
            f'\n{delimiter}{line}{delimiter}\n\n',
            **theme['color'],
        )

    def paragraph(self, text):
        """Rendering paragraph tags. Like ``<p>``."""
        return '%s\n' % text.strip(' ')

    def codespan(self, text):
        """Rendering inline `code` text.

        :param text: text content for inline code.
        """
        text = escape(text.rstrip(), smart_amp=False)
        theme = self._theme['code']
        return color(text, **theme)

    def linebreak(self):
        """Rendering line break like ``<br>``."""
        print('linebreak')
        return '\n'

    def text(self, text):
        """Rendering unformatted text.

        :param text: text content.
        """
        if self.options.get('parse_block_html'):
            return text
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

        theme = self._theme['table']
        line_color = theme['line_color']
        header_color = theme['header_color']
        line_color = theme['line_color']

        table = PrettyTable()
        first_row = self._table_rows[0]
        if first_row[0]['header']:
            table.field_names = [
                color(row['content'], **header_color) for row in first_row
            ]
            for col in first_row:
                align = col['align'][0] if col['align'] else 'l'
                content = color(col['content'], **header_color)
                table.align[content] = align
        for row_info in self._table_rows[1:]:
            table.add_row(
                [row['content'] for row in row_info]
            )
        result = table.get_string().splitlines()
        start = color(theme['top_left_char'], **line_color)
        end = color(theme['top_right_char'], **line_color)
        first_row = result[0][1:-1]
        first_row = first_row.replace(
            table.horizontal_char,
            color(theme['horizontal_char'], **line_color),
        )
        first_row = first_row.replace(
            table.junction_char,
            color(theme['top_junction_char'], **line_color),
        )

        lines = [
            f'{start}{first_row}{end}',
        ]
        for row in result[1:-1]:
            start = row[0]
            end = row[-1]
            inner = row[1:-1]

            if start == table.junction_char:
                start = color(theme['left_junction_char'], **line_color)
            else:
                start = color(theme['vertical_char'], **line_color)

            if end == table.junction_char:
                end = color(theme['right_junction_char'], **line_color)
            else:
                end = color(theme['vertical_char'], **line_color)

            inner = inner.replace(
                table.horizontal_char,
                color(theme['horizontal_char'], **line_color),
            )
            inner = inner.replace(
                table.vertical_char,
                color(theme['vertical_char'], **line_color),
            )
            inner = inner.replace(
                table.junction_char,
                color(theme['intersection_char'], **line_color),
            )

            lines.append(f'{start}{inner}{end}')

        start = color(theme['bottom_left_char'], **line_color)
        end = color(theme['bottom_right_char'], **line_color)
        last_row = result[-1][1:-1]
        last_row = last_row.replace(
            table.horizontal_char,
            color(theme['horizontal_char'], **line_color),
        )
        last_row = last_row.replace(
            table.junction_char,
            color(theme['bottom_junction_char'], **line_color),
        )
        lines.append(f'{start}{last_row}{end}')
        self._table_rows = None
        self._table_row = None
        return '\n'.join(lines)

    def table_row(self, content):
        if self._table_rows is None:
            self._table_rows = []
        self._table_rows.append(self._table_row)
        self._table_row = None
        return ''

    def table_cell(self, content, **flags):
        """Rendering a table cell. Like ``<th>`` ``<td>``.

        :param content: content of current table cell.
        :param header: whether this is header or not.
        :param align: align of current table cell.
        """
        header = flags['header']
        align = flags['align']

        if self._table_row is None:
            self._table_row = []

        self._table_row.append(
            {
                'header': header,
                'align': align,
                'content': content,
            },
        )
        return ''

    def escape(self, text):
        """Rendering escape sequence.

        :param text: text content.
        """
        return escape(text)

    def autolink(self, link, is_email=False):
        return self.link(link, '', link)

    def link(self, link, title, text):
        """Rendering a given link with content and title.

        :param link: href link for ``<a>`` tag.
        :param title: title content for `title` attribute.
        :param text: text content for description.
        """
        link = escape_link(link)
        theme = self._theme['link']
        start = theme['start_symbol']
        end = theme['end_symbol']
        text_color = theme['text_color']
        link_color = theme['link_color']
        text = color(text, **text_color)
        link = color(f' {start} {link} {end}', **link_color)
        return f'{text}{link}'

    def image(self, src, title, text):
        """Rendering a image with title and text.

        :param src: source link of the image.
        :param title: title text of the image.
        :param text: alt text of the image.
        """
        return ''

    def inline_html(self, html):
        """Rendering span level pure html content.

        :param html: text content of the html snippet.
        """
        return ''

    def newline(self):
        """Rendering newline element."""
        print('newline')
        return '\n'

    def footnote_ref(self, key, index):
        """Rendering the ref anchor of a footnote.

        :param key: identity key for the footnote.
        :param index: the index count of current footnote.
        """
        html = (
            '<sup class="footnote-ref" id="fnref-%s">'
            '<a href="#fn-%s">%d</a></sup>'
        ) % (escape(key), escape(key), index)
        return html

    def footnote_item(self, key, text):
        """Rendering a footnote item.

        :param key: identity key for the footnote.
        :param text: text content of the footnote.
        """
        back = (
            '<a href="#fnref-%s" class="footnote">&#8617;</a>'
        ) % escape(key)
        text = text.rstrip()
        if text.endswith('</p>'):
            text = re.sub(r'<\/p>$', r'%s</p>' % back, text)
        else:
            text = '%s<p>%s</p>' % (text, back)
        html = '<li id="fn-%s">%s</li>\n' % (escape(key), text)
        return html

    def footnotes(self, text):
        """Wrapper for all footnotes.

        :param text: contents of all footnotes.
        """
        html = '<div class="footnotes">\n%s<ol>%s</ol>\n</div>\n'
        return html % (self.hrule(), text)


def render(md):
    renderer = TerminalRenderer()
    data = markdown(md, renderer=renderer)
    print(data)


def test():
    md = """
> This is
> a blockquote
> OK

| Tables   |      Are      |  Cool |
|----------|:-------------:|------:|
| col 1 is |  left-aligned | $1600 |
| col 2 is |    centered   |   $12 |
| col 3 is | right-aligned |    $1 |


"""

    render(md)
