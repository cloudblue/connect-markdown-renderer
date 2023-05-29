from markdown_it import MarkdownIt
from rich.emoji import Emoji, NoEmoji
from rich.markdown import (
    BlockQuote,
    CodeBlock,
    HorizontalRule,
    ImageItem,
    ListElement,
    MarkdownContext,
    Paragraph,
    UnknownElement,
)
from rich.segment import Segment
from rich.style import Style

from connect.utils.terminal.markdown.components import (
    Heading,
    Link,
    ListItem,
    TableCellElement,
    TableElement,
    TableRowElement,
    TableSectionElement,
)
from connect.utils.terminal.markdown.emoji import emoji_plugin
from connect.utils.terminal.markdown.node import node_iterator


class GFContext(MarkdownContext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._emoji_context = False

    def enter_emoji(self):
        self._emoji_context = True

    def leave_emoji(self):
        self._emoji_context = False

    def on_text(self, text, node_type):
        if self._emoji_context:
            try:
                text = str(Emoji(text))
            except NoEmoji:
                text = f':{text}:'
        super().on_text(text, node_type)


class GFMarkdown:

    elements = {
        'paragraph': Paragraph,
        'heading': Heading,
        'fence': CodeBlock,
        'link': Link,
        'blockquote': BlockQuote,
        'hr': HorizontalRule,
        'ordered_list': ListElement,
        'bullet_list': ListElement,
        'list_item': ListItem,
        'image': ImageItem,
        'table': TableElement,
        'thead': TableSectionElement,
        'tbody': TableSectionElement,
        'tr': TableRowElement,
        'td': TableCellElement,
        'th': TableCellElement,
    }
    inlines = {'emph', 'strong', 'code', 's', 'code_inline'}

    def __init__(
        self,
        markup,
        code_theme='ansi_light',
    ):
        self.style = 'none'
        self.justify = 'left'
        self.markup = markup
        self.hyperlinks = False
        self.code_theme = code_theme
        parser = MarkdownIt().enable('strikethrough').enable('table').use(emoji_plugin)
        self.parsed = parser.parse(self.markup)

    def walker(self):
        return node_iterator(self.parsed)

    def __rich_console__(self, console, options):  # noqa: CCR001
        options = options.update(height=None)
        context = GFContext(console, options, Style())
        nodes = self.walker()
        inlines = self.inlines
        new_line = False
        root = UnknownElement.create(self, None)
        context.stack.push(root)
        for current, entering in nodes:
            node_type = current.type
            if node_type in ('html_inline', 'html_block', 'text'):
                context.on_text(current.literal.replace('\n', ' '), node_type)
            elif node_type == 'softbreak':  # pragma: no branch
                context.on_text(' ', node_type)
            elif node_type == 'emoji':
                if entering:
                    context.enter_emoji()
                else:
                    context.leave_emoji()
            elif node_type in inlines:
                if current.is_container():
                    if entering:
                        context.enter_style(f'markdown.{node_type}')
                    else:
                        context.leave_style()
                else:
                    context.enter_style(f'markdown.{node_type}')
                    if current.literal:
                        context.on_text(current.literal, node_type)
                    context.leave_style()
            else:
                element_class = self.elements.get(node_type) or UnknownElement
                if current.is_container():
                    if entering:
                        element = element_class.create(self, current)
                        context.stack.push(element)
                        element.on_enter(context)
                    else:
                        element = context.stack.pop()
                        if context.stack:
                            if context.stack.top.on_child_close(context, element):
                                if new_line:
                                    yield Segment('\n')
                                yield from console.render(element, context.options)
                                element.on_leave(context)
                            else:
                                element.on_leave(context)
                        else:
                            element.on_leave(context)
                            yield from console.render(element, context.options)
                        new_line = element.new_line
                else:
                    element = element_class.create(self, current)

                    context.stack.push(element)
                    element.on_enter(context)
                    if current.literal:
                        element.on_text(context, current.literal.rstrip())
                    context.stack.pop()
                    if context.stack.top.on_child_close(context, element):
                        if new_line:
                            yield Segment('\n')
                        yield from console.render(element, context.options)
                        element.on_leave(context)
                    else:
                        element.on_leave(context)
                    new_line = element.new_line
