
from markdown_it.rules_inline.state_inline import Delimiter


def tokenize(state, silent):
    start = state.pos
    marker = state.srcCharCode[start]

    if silent:  # pragma: no cover
        return False

    if marker != 0x3A:
        return False

    scanned = state.scanDelims(state.pos, marker == 0x3A)

    for i in range(scanned.length):
        token = state.push('text', '', 0)
        token.content = chr(marker)
        state.delimiters.append(
            Delimiter(
                marker=marker,
                length=scanned.length,
                jump=i,
                token=len(state.tokens) - 1,
                end=-1,
                open=scanned.can_open,
                close=scanned.can_close,
            ),
        )

    state.pos += scanned.length
    return True


def _post_process(state, delimiters):
    i = len(delimiters) - 1
    while i >= 0:
        start_delim = delimiters[i]

        if start_delim.marker != 0x3A:
            i -= 1
            continue

        if start_delim.end == -1:
            i -= 1
            continue

        end_delim = delimiters[start_delim.end]

        ch = chr(start_delim.marker)
        token = state.tokens[start_delim.token]
        token.type = 'emoji_open'
        token.tag = 'emoji'
        token.nesting = 1
        token.markup = ch
        token.content = ''

        token = state.tokens[end_delim.token]
        token.type = 'emoji_close'
        token.tag = 'emoji'
        token.nesting = -1
        token.markup = ch
        token.content = ''

        i -= 1


def post_process(state):
    _post_process(state, state.delimiters)
    for token in state.tokens_meta:
        if token and 'delimiters' in token:  # pragma: no cover
            _post_process(state, token['delimiters'])


def emoji_plugin(md):
    md.inline.ruler.before('emphasis', 'emoji', tokenize)
    md.inline.ruler2.before('emphasis', 'emoji', post_process)
