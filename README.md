# CloudBlue Connect Markdown Renderer


![pyversions](https://img.shields.io/pypi/pyversions/connect-markdown-renderer.svg) [![PyPi Status](https://img.shields.io/pypi/v/connect-markdown-renderer.svg)](https://pypi.org/project/connect-markdown-renderer/) [![Build Status](https://github.com/cloudblue/connect-markdown-renderer/workflows/Build%20Connect%20Markdown%20Renderer/badge.svg)](https://github.com/cloudblue/connect-markdown-renderer/actions) [![codecov](https://codecov.io/gh/cloudblue/connect-markdown-renderer/branch/master/graph/badge.svg)](https://codecov.io/gh/cloudblue/connect-markdown-renderer) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=markdown-renderer&metric=alert_status)](https://sonarcloud.io/dashboard?id=markdown-renderer)


## Introduction

`connect-markdown-renderer` is a small library that allow to render markdown documents in a terminal shell.


## Install

`connect-markdown-renderer` can be installed from pypi.org with pip:

```sh

$ pip install connect-markdown-renderer

```

## Usage example

```python

from connect.utils.terminal.markdown import render

my_md = """

# Heading level 1 - Paragraph

This is a paragraph with inline formatting like *italic*, **strong**, ~~strikethrough~~, `inline code` and :clapping_hands: emojis!.

## Heading level 2 - Lists

*Ordered list:*

1. First item
2. Second item
3. Third item

**Unordered list:**

* First
* Second
* Third

### Heading level 3 - blockquote

> This is a blockquote.
> > ...and a nested blockquote.


#### Heading level 4 - tables

| Col 1 | Col 2 | Col 3 |
|:------|:-----:|------:|
| a | b | c |


##### Heading level 5 - codeblock


```python

def this_is_my_python_function(args):
    return 'Hello World!'


"""

print(render(my_md))

```

This code will produce the following output:

![Console markdown](screenshot_1.png)



## Features

`connect-markdown-renderer` uses the new [markdown-it-py](https://github.com/executablebooks/markdown-it-py) parser and supports
[CommonMark](https://commonmark.org) plus the following extensions:

* tables
* strikethrough
* emoji

`connect-markdown-renderer` uses [rich](https://github.com/Textualize/rich) to render the markdown in the terminal.


## License

`connect-markdown-renderer` is released under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

