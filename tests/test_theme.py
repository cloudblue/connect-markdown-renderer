from connect.utils.terminal.markdown.theme import ConnectTheme


def test_theme():
    theme = ConnectTheme({
        'custom.style': 'red',
    })
    assert 'custom.style' in theme.styles
    assert 'markdown.strong' in theme.styles
    assert 'emphasize' in theme.styles
