import os
import sys
from datetime import datetime

import sphinx

from setuptools_scm import get_version


sys.path.insert(0, os.path.abspath('..'))

project = 'connect-markdown-renderer'
copyright = '{}, CloudBlue'.format(datetime.now().year)
author = 'CloudBlue'

release = get_version(root='..', relative_to=__file__)


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'm2r',
    'sphinx_copybutton',
]

autosectionlabel_prefix_document = True
autodoc_member_order = 'bysource'

source_suffix = ['.rst', '.md']

templates_path = ['_templates']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']


def monkeypatch(cls):
    def decorator(f):
        method = f.__name__
        old_method = getattr(cls, method)
        setattr(cls, method, lambda self, *args, **kwargs: f(old_method, self, *args, **kwargs))
    return decorator


# workaround until https://github.com/miyakogi/m2r/pull/55 is merged
@monkeypatch(sphinx.registry.SphinxComponentRegistry)
def add_source_parser(_old_add_source_parser, self, *args, **kwargs):
    # signature is (parser: Type[Parser], **kwargs), but m2r expects
    # the removed (str, parser: Type[Parser], **kwargs).
    if isinstance(args[0], str):
        args = args[1:]
    return _old_add_source_parser(self, *args, **kwargs)
