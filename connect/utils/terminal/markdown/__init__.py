from rich.console import Console

from connect.utils.terminal.markdown.renderer import GFMarkdown
from connect.utils.terminal.markdown.theme import ConnectTheme


def render(markup, theme=None, code_theme='ansi_light'):
    markdown = GFMarkdown(markup, code_theme=code_theme)
    console = Console(theme=theme or ConnectTheme())
    with console.capture() as capturer:
        console.print(markdown)
    return capturer.get()
