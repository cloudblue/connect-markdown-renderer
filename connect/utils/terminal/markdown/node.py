class Node:
    def __init__(self, token):
        self.token = token

    @property
    def justify(self):
        just = 'left'
        if 'style' in self.token.attrs:
            _, just = self.token.attrs['style'].split(':')
        return just

    @property
    def entering(self):
        return self.token.type.endswith('_open')

    @property
    def type(self):
        if self.token.type in ('em_open', 'em_close'):
            return 'emph'
        if self.token.type.endswith('_open') or self.token.type.endswith('_close'):
            return self.token.type.rsplit('_', 1)[0]
        return self.token.type

    @property
    def level(self):
        return len(self.token.markup)

    @property
    def list_data(self):
        if self.token.tag == 'ul':
            return {
                'type': 'bullet',
                'start': 1,
            }
        return {
            'type': 'number',
            'start': self.token.attrs.get('start', 1),
        }

    @property
    def destination(self):
        if self.token.type == 'link_open':
            return self.token.attrs['href']
        if self.token.type == 'image':
            return self.token.attrs['src']
        return ''

    @property
    def literal(self):
        return self.token.content

    @property
    def info(self):
        return self.token.info

    def is_container(self):
        return self.type in (
            'blockquote',
            'bullet_list',
            'ordered_list',
            'list_item',
            'paragraph',
            'heading',
            'emph',
            'strong',
            's',
            'link',
            'table',
            'thead',
            'tbody',
            'tr',
            'th',
            'td',
            'emoji',
        )


def node_iterator(tokens):
    for token in tokens:
        if token.type != 'inlines':
            wrapped = Node(token)
            yield wrapped, wrapped.entering
        if token.children:
            yield from node_iterator(token.children)
