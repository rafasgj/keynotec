"""Export the 'run' method."""

import sys
import os.path
import pkg_resources


def _run_xelatex(texfile):
    from subprocess import Popen, PIPE, STDOUT
    import os
    env = dict(os.environ)
    resources_dir = pkg_resources.resource_filename('keynotec', 'resources')
    env['TEXINPUTS'] = resources_dir + "//:"
    cmd = ['xelatex', '-interaction', 'nonstopmode', texfile]
    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT,
                 universal_newlines=True, env=env)
    for stream in proc.communicate():
        for line in stream.split('\n') if stream else []:
            if line and line[0] == '!':
                print("\n{}".format(line))


def run():
    """Run KeynoteC."""
    from keynotec.parser import parse_keynote

    if len(sys.argv) < 2:

        print("usage: keynotec <filename>")
        sys.exit(1)

    metabase = {
        'theme': "",
        'author': "",
        'institute': "",
        'date': "",
        'title': "",
        'subtitle': "",
        'language': "english",
        'slidenumber': "none",
        }

    filename = sys.argv[1]
    name, _ = os.path.splitext(filename)
    texfile = '{}.tex'.format(name)
    metadata_file = 'resources/metadata.inc'
    metafile = pkg_resources.resource_filename('keynotec', metadata_file)

    print("Processing {}...".format(filename), end='')
    with open(filename, 'rt') as datafile:
        keynote = parse_keynote((datafile.read(), 1))
    if keynote is None:
        raise Exception("Failed to load keynote data.")
    print(" done.")

    print("Preparing document...", end='')
    with open(texfile, 'wt') as output:
        output.write("\\input{presentation}")
        with open(metafile, 'rt') as meta:
            metabase.update(keynote.metadata)
            output.write(meta.read().format(**metabase))
        for plugin in keynote.plugins:
            output.write("\\input{{{plugin}}}".format(plugin=plugin))
        # page number
        slideoption = keynote.metadata['slidenumber']
        h, v = map(str.strip, slideoption.split(" ", 1))
        if h != "none":
            cfg = "\\setbeamertemplate{{{vertical}}}[{position} page number]"
            if h not in ['center', 'left', 'right']:
                raise Exception("Invalid slide number position: {}", h)
            if v not in ['top', 'bottom']:
                raise Exception("Invalid slide number position: {}", v)
            vertical = "headline" if v == "top" else "footline"
            output.write(cfg.format(vertical=vertical, position=h))
        # print slides
        output.write('\\begin{document}')
        for type, data in keynote.slides:
            output.write(data)
        output.write('\\end{document}')
    print(" done.")

    print("Creating slides...", end='')
    _run_xelatex(texfile)
    print(" done.")

    print("Fixing references and effects...", end='')
    _run_xelatex(texfile)
    print(" done.")

    print("Cleaning up...", end='')
    for ext in ['aux', 'log', 'nav', 'out', 'snm', 'toc', 'vrb', 'tex']:
        fname = '{}.{}'.format(name, ext)
        if os.access(fname, os.F_OK):
            os.unlink(fname)
    print("done.")

    if os.access('{}.pdf'.format(name), os.F_OK):
        print('{}.pdf'.format(name), "generated.")
