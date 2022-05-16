from rich.theme import Theme


class ConnectTheme(Theme):
    def __init__(self, styles=None, inherit=True):
        _styles = {
            'markdown.strong': 'bold bright_white',
            'markdown.emph': 'italic bright_white',
            'markdown.s': 'strike red',
            'markdown.code_inline': 'bright_white on black',
            'markdown.table.border': 'blue',
            'markdown.table.header': 'deep_sky_blue1',
            'markdown.h1': 'dodger_blue2',
            'markdown.h2': 'deep_sky_blue3',
            'markdown.h3': 'deep_sky_blue1',
            'markdown.h4': 'turquoise2',
            'markdown.h5': 'cornflower_blue',
            'markdown.h6': 'steel_blue1',
        }
        if styles is not None:
            _styles.update(styles)

        super().__init__(styles=_styles, inherit=inherit)
