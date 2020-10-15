from cmr.tables import TableRenderer


def test_render():
    expected = '\n'.join([
        '┌────────────┬────────────────┬──────┐',
        '│left        │     center     │ right│',
        '├────────────┼────────────────┼──────┤',
        '│val1        │      cen1      │right1│',
        '│left value 1│centered value 2│    r3│',
        '└────────────┴────────────────┴──────┘'
    ])

    t = TableRenderer()
    t.add_header_cell('left', 'left')
    t.add_header_cell('center', 'center')
    t.add_header_cell('right', 'right')
    t.add_cell('val1')
    t.add_cell('cen1')
    t.add_cell('right1')
    t.new_row()
    t.add_cell('left value 1')
    t.add_cell('centered value 2')
    t.add_cell('r3')
    t.new_row()
    assert t.render() == expected
