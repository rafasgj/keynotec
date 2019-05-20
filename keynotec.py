"""A recursive descendent parser for a keynote DSL."""

from string import ascii_letters, digits, whitespace


letters = {c for c in ascii_letters}
numbers = {d for d in digits}


class Keynote:
    """Hold keynote data."""

    def __init__(self):
        """Initialize an empty keynote."""
        self.metadata = {}
        self.slides = []
        self.plugins = []


keynote = Keynote()


def parse_keynote(data):
    """keynote: metadata slide+."""
    metadata, data = parse_metadata(data)
    keynote.metadata = metadata
    while True:
        slide, data = parse_slide(data)
        if not slide:
            break
        keynote.slides.append(slide)
        data = skip_space(data)
    if not keynote.slides:
        raise Exception("No slide was defined.")

    content, line = data
    if content:
        error = "There should be no input left at line {}"
        raise Exception(error.format(line))
    return keynote


def parse_metadata(data):
    """metadata: metadata_key value."""
    data = skip_space(data)
    metadata = {}
    while True:
        key, data = parse_metadata_key(data)
        if key is None:
            return [metadata, data]
        metadata[key], data = parse_metadata_value(data)


def parse_metadata_key(data):
    """
    Parse a metadata key.

    A metadata key can be one of 'theme', 'author', 'institute',
    'date', 'title', 'subtitle', 'language'.
    """
    content, line = data
    valid_keys = ['theme', 'author', 'institute', 'date',
                  'title', 'subtitle', 'language']
    token, data = next_token(data)
    if token in valid_keys:
        return [token, data]
    else:
        return [None, (content, line)]


def parse_metadata_value(data):
    """Parse a metadata value: ':' STRING."""
    content, line = skip_space(data)
    if content[0] != ":":
        raise Exception("Expected ':' at line", line)
    content, line = skip_space((content[1:], line))
    return parse_STRING((content, line))


def parse_slide(data):
    """slide: ":" slide_type (slide_arguments)? (slide_content)?."""
    type, data = parse_slide_type(data)
    if type is None:
        return [None, data]
    # TYPES: parse proprer slide type.
    slide_parser = {
        'coverpage': parse_slide_coverpage,
        'bigtitle': parse_slide_bigtitle,
        'citation': parse_slide_citation,
        'bigimage': parse_slide_bigimage,
        'twoimages': parse_slide_twoimages,
        'fourimages': parse_slide_fourimages,
        'code': parse_slide_code,
        'items': parse_slide_items,
    }
    if type not in slide_parser:
        error = "Invalid slide type '{}' at line {}"
        raise Exception(error.format(type, data[1]))
    data = skip_space(data)
    slide, data = slide_parser[type](data)
    return [(type, slide), data]


def parse_slide_type(data):
    """slide_type: ":" STRING."""
    content, line = skip_space(data)
    if not content:
        return [None, (None, line)]
    if content[0] != ":":
        raise Exception("Expected ':' at line", line)
    return parse_STRING((content[1:], line))


def parse_slide_coverpage(data):
    """There's no data for coverpage."""
    # Nothing to do in coverpage.
    return ['\\coverframe', data]


def parse_slide_bigtitle(data):
    """Bigtitle only has a title."""
    title, (content, line) = parse_title(data)
    if title is None:
        raise Exception("Expected '#' at line", line)
    fmt = '\\bigtitle{{{}}}'
    return [fmt.format(title), (content, line)]


def parse_slide_citation(data):
    """Bigtitle only has a title."""
    citation, data = parse_title(data)
    author, data = parse_cite(data)
    fmt = '\\citation{{{}}}{{{}}}'
    return [fmt.format(citation, author), data]


def parse_slide_bigimage(data):
    """Bigtitle only has a title."""
    image, data = parse_image(data)
    fmt = '\\bigimage{{{}}}'
    return [fmt.format(image), data]


def parse_slide_twoimages(data):
    """Bigtitle only has a title."""
    imageleft, data = parse_image(data)
    data = skip_space(data)
    imageright, data = parse_image(data)
    fmt = '\\twoimages{{{}}}{{{}}}'
    return [fmt.format(imageleft, imageright), data]


def parse_slide_fourimages(data):
    """Bigtitle only has a title."""
    images = [''] * 4
    for i in range(4):
        images[i], data = parse_image(data)
        data = skip_space(data)
    fmt = '\\fourimages{{{}}}{{{}}}{{{}}}{{{}}}'
    return [fmt.format(*images), data]


def parse_slide_code(data):
    """code: (title)? '```' code_block '```'."""
    title, data = parse_title(data)
    data = skip_space(data)
    (language, code), data = parse_code_block(data)
    keynote.plugins.append('listings/{}'.format(language))
    frame = """\\begin{{frame}}[fragile]
        \\frametitle{{{title}}}\n{content}\n\\end{{frame}}
    """
    template = """\\begin{{{language}}}\n{code}\n\\end{{{language}}}"""
    content = template.format(language=language, code=code)
    return [frame.format(title=title if title is not None else "",
                         content=content), data]


def parse_code_block(data):
    """code_block: "```" STRING /.*?(?=```)/ "```"."""
    content, line = data
    if content[0:3] != "```":
        raise Exception("Expected '```' at line {}.".format(line))
    lang, (content, line) = parse_STRING((content[3:], line))
    line += 1
    i = 1
    while i < len(content)-3 and content[i:i+3] != '```':
        if content[i] == '\n':
            line += 1
        i += 1
    value = content[1:i]
    # skip closing '```'.
    return [(lang, value), (content[i+3:], line)]


def parse_slide_items(data):
    """items: "items" title? itemlist."""
    title, (content, line) = parse_title(data)
    if title is None:
        title = ""
    else:
        # skip title command line
        data = content[1:], line + 1
    items, data = parse_itemlist(data)
    # TODO: process items.
    last, items = items
    start, end = "\\begin{itemize}", "\\end{itemize}"
    result = start
    stack = [end]
    for ident, item in items:
        if ident < last:
            result += stack.pop()
            last = ident
        elif ident > last:
            stack.append(end)
            result += start
            last = ident
        result += "\\item {}".format(item)
    while stack:
        result += stack.pop()
    data = skip_space(data)
    frame = """\\begin{{frame}}\n\\frametitle{{{title}}}
               {items}\n\\end{{frame}}\n"""
    frame = frame.format(title=title, items=result)
    return [frame, data]


# -- general item parsig functions --

def parse_itemlist(data):
    """itemlist: singleitem (singleitem)+."""
    content, line = data
    items = []
    min = 0
    while True:
        item, (content, line) = parse_singleitem((content, line))
        if item is None:
            break
        if not items:
            min = item[0]
        else:
            if item[0] < min:
                e = "Items cannot have less identation than first item"
                raise Exception((e + " at line {}").format(line))
        items.append(item)
    return [(min, items), (content, line)]


def parse_singleitem(data):
    """singleitem: level "*" STRING."""
    content, line = data
    i = 0
    while i < len(content) and content[i] == " ":
        i += 1
    if i == len(content):
        return [None, (None, line)]
    if content[i] != '*':
        raise Exception("Expected '*' for item list an line {}.".format(line))
    data = skip_space((content[i+1:], line))
    item, (content, line) = parse_STRING(data)
    # skip next line marker.
    return [(i, item), (content[1:], line + 1)]


def parse_STRING(data):
    r"""STRING: ([^\\n]*)\\n."""
    content, line = data
    i = 0
    while i < len(content) and content[i] != '\n':
        i += 1
    value = content[:i].strip()
    return [value, (content[i:], line)]


def parse_image(data):
    r"""image: \[([^]+)\]."""
    content, line = data
    if content[0] != '[':
        raise Exception("Expecting '[' to parse image at line {}".format(line))
    i = 0
    while i < len(content) and content[i] != ']':
        i += 1
    if not i < len(content):
        error = "Image open at end of file (from line {})"
        raise Exception(error.format(line))
    value = content[1:i]
    # skip closing ']' by starting at next character.
    return [value, (content[i + 1:], line)]


def parse_title(data):
    """title: # STRING."""
    content, line = skip_space(data)
    if content[0] != "#":
        return [None, data]
    if len(content) > 1 and content[1] not in {' ', '\t'}:
        raise Exception("Expected a whitespace after '#' at line", line)
    return parse_STRING((content[2:], line))


def parse_cite(data):
    """title: # STRING."""
    content, line = skip_space(data)
    if len(content) < 2:
        raise Exception("Expected citation author at line {}.", line)
    if content[0] != "-" and content[1] != '-':
        raise Exception("Expected '--' at line", line)
    return parse_STRING((content[2:], line))


# -- general parsing functions --

def skip_space(data):
    """Skip white space in input."""
    content, line = data
    if not content:
        return None, (None, line)
    i = 0
    while i < len(content) and content[i] in whitespace:
        if content[i] == '\n':
            line += 1
        i += 1
    return [content[i:], line]


def next_token(data):
    """Extract next token from input."""
    content, line = skip_space(data)
    if not content:
        return None, [None, line]
    i = 0
    while i < len(content) and content[i] in (letters | numbers):
        i += 1
    return content[:i].strip(), [content[i:], line]


# -- main()

if __name__ == "__main__":
    import sys
    metabase = {
        'theme': "",
        'author': "",
        'institute': "",
        'date': "",
        'title': "",
        'subtitle': "",
        'language': "english",
        }
    with open(sys.argv[1], 'rt') as datafile:
        keynote = parse_keynote((datafile.read(), 1))
    if keynote is None:
        raise Exception("Failed to load keynote data.")
    with open('template/out.tex', 'wt') as output:
        output.write("\\input{presentation}")
        with open('template/metadata.inc', 'rt') as meta:
            metabase.update(keynote.metadata)
            output.write(meta.read().format(**metabase))
        for plugin in keynote.plugins:
            output.write("\\input{{{plugin}}}".format(plugin=plugin))
        output.write('\\begin{document}')
        for type, data in keynote.slides:
            output.write(data)
        output.write('\\end{document}')
