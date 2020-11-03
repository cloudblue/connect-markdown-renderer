from colors import color


class TableRenderer:

    def __init__(self, **kwargs):
        self._horizontal_char = kwargs.get('horizontal_char', '─')
        self._vertical_char = kwargs.get('vertical_char', '│')
        self._intersection_char = kwargs.get('intersection_char', '┼')
        self._top_left_char = kwargs.get('top_left_char', '┌')
        self._top_right_char = kwargs.get('top_right_char', '┐')
        self._bottom_left_char = kwargs.get('bottom_left_char', '└')
        self._bottom_right_char = kwargs.get('bottom_right_char', '┘')
        self._left_junction_char = kwargs.get('left_junction_char', '├')
        self._right_junction_char = kwargs.get('right_junction_char', '┤')
        self._top_junction_char = kwargs.get('top_junction_char', '┬')
        self._bottom_junction_char = kwargs.get('bottom_junction_char', '┴')
        self._line_color = kwargs.get('line_color', {})
        self._header_color = kwargs.get('header_color', {})
        self._cell_color = kwargs.get('cell_color', {})
        self._header = []
        self._align = []
        self._rows = []
        self._current_row = []
        self._another = []

    def add_header_cell(self, value, align):
        self._header.append(value)
        self._align.append(align or 'left')

    def add_cell(self, value):
        self._current_row.append(value)

    def new_row(self):
        if self._current_row:
            self._rows.append(self._current_row)
            self._current_row = []

    def _get_col_widths(self):
        widths = []
        rows = self._rows[:]
        if self._header:
            rows.insert(0, self._header)
        widths = [0 for _ in range(len(rows[0]))]
        for row in rows:
            for idx, col in enumerate(row):
                if widths[idx] < len(col):
                    widths[idx] = len(col)
        return widths

    def _render_header(self, col_widths, horizontal_lines, vertical_sym):
        values = []
        for idx, val in enumerate(self._header):
            justified_value = ''
            size = col_widths[idx]
            if self._align[idx] == 'right':
                justified_value = val.rjust(size)
            elif self._align[idx] == 'center':
                justified_value = val.center(size)
            else:
                justified_value = val.ljust(size)
            values.append(
                color(justified_value, **self._header_color)
            )
        return [
            vertical_sym + vertical_sym.join(values) + vertical_sym,
            color(self._left_junction_char, **self._line_color)
            + color(self._intersection_char, **self._line_color).join(horizontal_lines)
            + color(self._right_junction_char, **self._line_color),            
        ]

    def render(self):
        col_widths = self._get_col_widths()
        if not self._align:
            self._align = ['left' for _ in range(len(col_widths))]

        vertical_sym = color(self._vertical_char, **self._line_color)
        horizontal_lines = [
            color(self._horizontal_char * w, **self._line_color)
            for w in col_widths
        ]
        lines = []
        lines.append(
            color(self._top_left_char, **self._line_color)
            + color(self._top_junction_char, **self._line_color).join(horizontal_lines)
            + color(self._top_right_char, **self._line_color)
        )
        if self._header:
            lines.extend(self._render_header(col_widths, horizontal_lines, vertical_sym))

        for row in self._rows:
            values = []
            for idx, val in enumerate(row):
                justified_value = ''
                size = col_widths[idx]
                if self._align[idx] == 'right':
                    justified_value = val.rjust(size)
                elif self._align[idx] == 'center':
                    justified_value = val.center(size)
                else:
                    justified_value = val.ljust(size)
                values.append(
                    color(justified_value, **self._cell_color)
                )
            lines.append(vertical_sym + vertical_sym.join(values) + vertical_sym)

        lines.append(
            color(self._bottom_left_char, **self._line_color)
            + color(self._bottom_junction_char, **self._line_color).join(horizontal_lines)
            + color(self._bottom_right_char, **self._line_color)
        )
        return '\n'.join(lines)
