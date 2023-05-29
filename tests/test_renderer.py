from io import StringIO

from rich.console import Console

from connect.utils.terminal.markdown.renderer import GFMarkdown
from connect.utils.terminal.markdown.theme import ConnectTheme


def test_inlines():
    console = Console(
        theme=ConnectTheme(),
        file=StringIO(),
        force_terminal=True,
        width=132,
        color_system='standard',
    )
    console.print(
        GFMarkdown(
            'Text with *italic* and **bold** ~~strikethrough~~ `code` :clapping_hands:',
        ),
    )
    assert console.file.getvalue() == open('tests/data/inlines').read()


def test_unknown_emoji():
    console = Console(
        theme=ConnectTheme(),
        file=StringIO(),
        force_terminal=True,
        width=132,
        color_system='standard',
    )
    console.print(GFMarkdown(':unknown_emoji:'))
    assert console.file.getvalue().strip() == ':unknown_emoji:'


def test_headings():
    console = Console(
        theme=ConnectTheme(),
        file=StringIO(),
        force_terminal=True,
        width=132,
        color_system='standard',
    )
    console.print(GFMarkdown('\n'.join(['#' * i + f' Level {i}' for i in range(1, 7)])))
    assert console.file.getvalue() == open('tests/data/headings').read()


def test_unordered_list():
    console = Console(
        theme=ConnectTheme(),
        file=StringIO(),
        force_terminal=True,
        width=132,
        color_system='standard',
    )
    console.print(GFMarkdown('\n'.join([f'* bullet {i}' for i in range(3)])))
    assert console.file.getvalue() == open('tests/data/unordered_list').read()


def test_ordered_list():
    console = Console(
        theme=ConnectTheme(),
        file=StringIO(),
        force_terminal=True,
        width=132,
        color_system='standard',
    )
    console.print(GFMarkdown('\n'.join([f'{i}. ordered {i}' for i in range(3)])))
    assert console.file.getvalue() == open('tests/data/ordered_list').read()


def test_link():
    console = Console(
        theme=ConnectTheme(),
        file=StringIO(),
        force_terminal=True,
        width=132,
        color_system='standard',
    )
    console.print(GFMarkdown('[Google](https://google.com)'))
    assert console.file.getvalue() == open('tests/data/link').read()


def test_image():
    console = Console(
        theme=ConnectTheme(),
        file=StringIO(),
        force_terminal=True,
        width=132,
        color_system='standard',
    )
    console.print(GFMarkdown('![Image](image.png)'))
    assert console.file.getvalue() == open('tests/data/image').read()


def test_table():
    table = """
| Col 1 | Col 2 | Col 3 |
|:------|:-----:|------:|
| a | b | c |
"""
    console = Console(
        theme=ConnectTheme(),
        file=StringIO(),
        force_terminal=True,
        width=132,
        color_system='standard',
    )
    console.print(GFMarkdown(table))
    assert console.file.getvalue() == open('tests/data/table').read()


def test_code_block():
    code = """```python
    def my_function(args):
        pass
"""
    console = Console(
        theme=ConnectTheme(),
        file=StringIO(),
        force_terminal=True,
        width=132,
        color_system='standard',
    )
    console.print(GFMarkdown(code))
    assert console.file.getvalue() == open('tests/data/code_block').read()


def test_block_quote():
    block_quote = """> pippo
> > pippo 2
> > > pippo 3
"""
    console = Console(
        theme=ConnectTheme(),
        file=StringIO(),
        force_terminal=True,
        width=132,
        color_system='standard',
    )
    console.print(GFMarkdown(block_quote))
    assert console.file.getvalue() == open('tests/data/block_quote').read()


def test_breaks():
    breaks = """Line 1

Line 2

Line 3

<br>

Line4 long paragram
fdsofdkokfdofdkfoodkf
dofdofkdokfodkfodkfd"""

    console = Console(
        theme=ConnectTheme(),
        file=StringIO(),
        force_terminal=True,
        width=132,
        color_system='standard',
    )
    console.print(GFMarkdown(breaks))
    assert console.file.getvalue() == open('tests/data/breaks').read()
