import pytest

from colors import color

from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers import get_lexer_by_name

from cmr.renderer import TerminalRenderer, render
from cmr.tables import TableRenderer
from cmr.theme import DEFAULT_THEME


def test_headings():
    renderer = TerminalRenderer()
    for level in range(1, 7):
        value = renderer.header('Text', level)
        colors = DEFAULT_THEME['headings'][level]
        assert value == color('Text\n\n', **colors)


@pytest.mark.parametrize(
    ('method', 'style', 'text', 'expected'),
    (
        ('double_emphasis', 'strong', 'Text', 'Text'),
        ('emphasis', 'em', 'Text', 'Text'),
        ('codespan', 'code', 'Text', 'Text'),
        ('strikethrough', 'del', 'Text', 'T\u0336e\u0336x\u0336t\u0336'),
    )
)
def test_inlines(method, style, text, expected):
    renderer = TerminalRenderer()
    call = getattr(renderer, method)
    value = call(text)

    colors = DEFAULT_THEME[style]
    assert value == color(expected, **colors)


def test_hrule(mocker):
    mocker.patch('shutil.get_terminal_size', return_value=(80, 24))
    renderer = TerminalRenderer()
    value = renderer.hrule()
    theme = DEFAULT_THEME['hr']
    delimiter = theme['delimiter']
    line = theme['line']
    colors = theme['color']
    hr = '\n' + delimiter + (line * 78) + delimiter + '\n\n'
    assert value == color(hr, **colors)


def test_paragraph():
    renderer = TerminalRenderer()
    text = '  Text   '
    value = renderer.paragraph(text)

    colors = DEFAULT_THEME['p']
    assert value == color('Text', **colors) + '\n\n'


def test_text():
    renderer = TerminalRenderer()
    value = renderer.text('Text')
    assert value == 'Text'


@pytest.mark.parametrize(
    ('method', 'args'),
    (
        ('block_html', ('html',)),
        ('inline_html', ('html',)),
        ('footnotes', ('text',)),
        ('footnote_item', ('key', 'text')),
        ('footnote_ref', ('key', 'text')),
    )
)
def test_not_supported(method, args):
    renderer = TerminalRenderer()
    call = getattr(renderer, method)
    assert call(*args) == ''


def test_newline_linebreak():
    renderer = TerminalRenderer()
    assert renderer.newline() == '\n'
    assert renderer.linebreak() == '\n'


def test_list_item():
    renderer = TerminalRenderer()
    assert renderer.list_item('Text') == 'Text\n'


def test_ordered_list():
    renderer = TerminalRenderer()
    ordered_list = renderer.list(
        'First\nSecond\nThird\n',
        ordered=True,
    )
    separator = DEFAULT_THEME['ol']['separator']
    colors = DEFAULT_THEME['ol']['color']
    expected = '\n'.join(
        [
            color(f'  1{separator}First', **colors),
            color(f'  2{separator}Second', **colors),
            color(f'  3{separator}Third', **colors),
        ]
    ) + '\n\n'

    assert ordered_list == expected


def test_unordered_list():
    renderer = TerminalRenderer()
    ordered_list = renderer.list(
        'First\nSecond\nThird\n',
        ordered=False,
    )
    symbol = DEFAULT_THEME['ul']['symbol']
    separator = DEFAULT_THEME['ul']['separator']
    colors = DEFAULT_THEME['ul']['color']
    expected = '\n'.join(
        [
            color(f'  {symbol}{separator}First', **colors),
            color(f'  {symbol}{separator}Second', **colors),
            color(f'  {symbol}{separator}Third', **colors),
        ]
    ) + '\n\n'

    assert ordered_list == expected


def test_link():
    renderer = TerminalRenderer()

    text = 'This is a link'
    link = 'https://example.com'

    output = renderer.link(link, text, text)

    start = DEFAULT_THEME['a']['start_symbol']
    end = DEFAULT_THEME['a']['end_symbol']
    text_color = DEFAULT_THEME['a']['text_color']
    link_color = DEFAULT_THEME['a']['link_color']

    text = color(text, **text_color)
    link = color(f' {start} {link} {end}', **link_color)
    assert output == f'{text}{link}'


def test_image():
    renderer = TerminalRenderer()

    text = 'This is an image'
    link = 'https://example.com/image.png'

    output = renderer.image(link, text, text)

    start = DEFAULT_THEME['img']['start_symbol']
    end = DEFAULT_THEME['img']['end_symbol']
    text_color = DEFAULT_THEME['img']['text_color']
    link_color = DEFAULT_THEME['img']['link_color']

    text = color(text, **text_color)
    link = color(f' {start} {link} {end}', **link_color)
    assert output == f'{text}{link}'


def test_autolink():
    renderer = TerminalRenderer()

    link = 'https://example.com'

    output = renderer.autolink(link)

    start = DEFAULT_THEME['a']['start_symbol']
    end = DEFAULT_THEME['a']['end_symbol']
    text_color = DEFAULT_THEME['a']['text_color']
    link_color = DEFAULT_THEME['a']['link_color']
    text = color(link, **text_color)
    link = color(f' {start} {link} {end}', **link_color)
    assert output == f'{text}{link}'


def test_blockquote():
    renderer = TerminalRenderer()
    colors = DEFAULT_THEME['blockquote']['color']
    symbol = DEFAULT_THEME['blockquote']['symbol']
    sep = DEFAULT_THEME['blockquote']['separator']
    indent = DEFAULT_THEME['blockquote']['indent']
    expected = '\n\n' + '\n'.join([
        color(f'{indent}{symbol}{sep}{line}', **colors)
        for line in ('first', 'second', 'third')
    ]) + '\n\n'
    assert renderer.block_quote('first\nsecond\nthird\n\n') == expected


def test_blockcode():
    renderer = TerminalRenderer()
    lexer = get_lexer_by_name('python')
    highlighted = highlight(
        'def myfunc():\n    pass\n',
        lexer,
        TerminalFormatter(bg='dark'),
    )
    expected = '\n' + highlighted + '\n'

    assert renderer.block_code(
        'def myfunc():\n    pass\n',
        'python',
    ) == expected


def test_table_cell(mocker):
    mock = mocker.patch.object(TableRenderer, 'add_cell')
    renderer = TerminalRenderer()
    renderer.table_cell('value', align='left', header=False)
    assert mock.called_once_with('value')


def test_table_header_cell(mocker):
    mock = mocker.patch.object(TableRenderer, 'add_header_cell')
    renderer = TerminalRenderer()
    renderer.table_cell('value', align='left', header=True)
    assert mock.called_once_with('value', 'left')


def test_table_row(mocker):
    mock = mocker.patch.object(TableRenderer, 'new_row')
    renderer = TerminalRenderer()
    renderer.table_cell('value', align='left', header=False)
    assert mock.not_called()
    renderer.table_row('')
    assert mock.called_once()


def test_table(mocker):
    mock = mocker.patch.object(TableRenderer, 'render')
    renderer = TerminalRenderer()
    renderer.table_cell('value', align='left', header=False)
    renderer.table_row('')
    renderer.table('', '')
    assert mock.called_once()


def test_escape(mocker):
    mock = mocker.patch('cmr.renderer.escape')
    renderer = TerminalRenderer()
    renderer.escape('<test>')
    assert mock.called_once_with('<test>')


def test_render():
    md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6


Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque pulvinar
sagittis lectus, rhoncus faucibus ante molestie ac. *Fusce et erat at dolor
pretium bibendum vitae a libero.* Nullam efficitur tincidunt enim. Donec
pretium nisi in orci laoreet fermentum at fermentum erat. Aliquam sodales
eget enim vitae ullamcorper. Vivamus iaculis nulla sed mi malesuada
consectetur.
Nam malesuada porta tellus, eu faucibus ante congue sed. Vestibulum et
justo id nisi pretium pretium. Nam finibus nec sapien a ultrices. In a
porttitor neque, vel sodales nibh. Aliquam eu felis vel nisi ullamcorper
vulputate. Phasellus ut feugiat dui. Fusce a dictum lacus. Donec sed dui
feugiat, dignissim eros sed, scelerisque nunc.

Maecenas at velit pretium libero ullamcorper finibus. **Vivamus vel velit
quis erat rhoncus convallis.** Mauris viverra suscipit eros, eget molestie
tortor fermentum sodales.
Proin porta ullamcorper ornare. Morbi sed lectus tempor, sollicitudin
elit non, scelerisque odio.
Mauris at molestie sem. Vivamus sed mi lacus. Morbi sed mauris nec massa
pulvinar auctor a vel augue. Maecenas quis elementum enim. Nullam enim lacus,
dictum et gravida et, luctus pretium lorem. Praesent finibus ex sit amet ante
elementum cursus. Sed in est ac libero sagittis tempor. Morbi pulvinar
facilisis tellus vel hendrerit. Maecenas fermentum ex non lectus ultricies
congue. Curabitur laoreet eu eros at pretium. Vivamus hendrerit dignissim
tortor, at rhoncus eros porttitor nec.

-----



| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |


> This is a block
> Second block line
> Third block line


* Bullet list 1
* Bullet list 2
* Bullet list 3


1. Ordered list 1
2. Ordered list 2
3. Ordered list 3


This is **strong**

This is *italic*

This is ~~striketrough~~

[This is a link](https://google.com)


![alt text](https://example.com/image.jpg "Logo Title Text 1")
"""
    rendered = render(md, theme=None)

    assert rendered is not None
    assert rendered != ''
