from connect.utils.terminal.markdown import render


def test_render(mocker):
    mocked_theme = mocker.MagicMock()
    mocker.patch('connect.utils.terminal.markdown.ConnectTheme', return_value=mocked_theme)
    mocked_console = mocker.MagicMock()
    mocked_capturer = mocker.MagicMock()
    mocked_capturer.get.return_value = 'captured'
    mocked_console.capture.return_value.__enter__.return_value = mocked_capturer
    mocked_markdown = mocker.patch('connect.utils.terminal.markdown.GFMarkdown')
    console_mock = mocker.patch('connect.utils.terminal.markdown.Console', return_value=mocked_console)
    assert render('this *is* markdown!') == 'captured'
    mocked_markdown.assert_called_once_with('this *is* markdown!', code_theme='ansi_light')
    console_mock.assert_called_once_with(theme=mocked_theme)
