from rich import box
from rich.markdown import (
    Heading as _Heading,
    ListItem as _ListItem,
    MarkdownElement,
    TextElement,
)
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text


class TableElement(MarkdownElement):
    new_line = False

    @classmethod
    def create(cls, markdown, node):
        return cls()

    def __init__(self) -> None:
        self.thead = None
        self.tbody = None

    def on_child_close(self, context, child):
        assert isinstance(child, TableSectionElement)
        if child.section_type == 'thead':
            self.thead = child
        else:
            self.tbody = child
        return False

    def __rich_console__(self, console, options):
        border_style = console.get_style('markdown.table.border', default='none')
        header_style = console.get_style('markdown.table.header', default='none')
        body_style = console.get_style('markdown.table.body', default='none')
        t = Table(
            box=box.ROUNDED,
            border_style=border_style,
            header_style=header_style,
        )
        for col in self.thead.rows[0].cells:
            t.add_column(col.text, style=body_style)
        for row in self.tbody.rows:
            t.add_row(*[item.text for item in row.cells])
        yield t


class TableSectionElement(MarkdownElement):
    new_line = False

    @classmethod
    def create(cls, markdown, node):
        return cls(node)

    def __init__(self, node):
        self.section_type = node.type
        self.rows = []

    def on_child_close(self, context, child):
        assert isinstance(child, TableRowElement)
        self.rows.append(child)
        return False


class TableRowElement(MarkdownElement):
    new_line = False

    @classmethod
    def create(cls, markdown, node):
        return cls()

    def __init__(self) -> None:
        self.cells = []

    def on_child_close(self, context, child):
        assert isinstance(child, TableCellElement)
        self.cells.append(child)
        return False


class TableCellElement(TextElement):
    new_line = False

    @classmethod
    def create(cls, markdown, node):
        return cls(node)

    def __init__(self, node) -> None:
        self.justify = node.justify

    def on_text(self, context, text):
        super().on_text(context, text)
        self.text.justify = self.justify


class Link(TextElement):

    @classmethod
    def create(cls, markdown, node):
        return cls(node)

    def __init__(self, node):
        self.destination = node.destination

    def __rich_console__(self, console, options):
        link_style = console.get_style('markdown.link')
        url_style = console.get_style('markdown.link_url') + Style(underline=True)
        self.text.style = link_style

        self.text += Text(" (", style=link_style)
        self.text += Text(self.destination, style=url_style)
        self.text += Text(")", style=link_style)
        yield self.text


class ListItem(_ListItem):
    new_line = False


class Heading(_Heading):
    def __rich_console__(self, console, options):
        text = self.text
        text.justify = "center"
        if self.level == 1:
            yield Panel(
                text,
                box=box.ROUNDED,
                style="markdown.h1.border",
            )
        else:
            if self.level == 2:
                yield Text("")
            yield text
