"""Export the 'run' method."""

import sys
import os.path
import pkg_resources


metabase = {
    'theme': "",
    'author': "",
    'institute': "",
    'date': "",
    'title': "",
    'subtitle': "",
    'language': "english",
    'slidenumber': "none none",
    'fullscreen': False,
    }


def _run_xelatex(texfile):
    from subprocess import Popen, PIPE, STDOUT
    import os
    env = dict(os.environ)
    resources_dir = pkg_resources.resource_filename('keynotec', 'resources')
    env['TEXINPUTS'] = resources_dir + "//:"
    cmd = ['xelatex', '-interaction', 'nonstopmode', texfile]
    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT,
                 universal_newlines=True, env=env)
    error = False
    for stream in proc.communicate():
        for line in stream.split('\n') if stream else []:
            if line and line[0] == '!':
                error = True
                print("\n{}".format(line))
    return error


def _generate_pagenumber(keynote, output):
    """Configure slide number, if needed."""
    # page number
    slideoption = keynote.metadata.get('slidenumber', "none none")
    h, *v = map(str.strip, slideoption.split(" ", 1))
    v = " ".join(v)
    if h != "none":
        cfg = "\\setbeamertemplate{{{vertical}}}[{position} page number]"
        if h not in ['center', 'left', 'right']:
            raise Exception("Invalid slide number position: {}", h)
        if v not in ['top', 'bottom']:
            raise Exception("Invalid slide number position: {}", v)
        vertical = "headline" if v == "top" else "footline"
        output.write(cfg.format(vertical=vertical, position=h))


def _generate_fullscreen(keynote, output):
    """Configure keynote to open in full screen automatically."""
    if keynote.metadata.get('fullscreen', False):
        output.write('\\hypersetup{pdfpagemode=FullScreen}')


def run():
    """Run KeynoteC."""
    from keynotec.parser import parse_keynote

    if len(sys.argv) < 2:

        print("usage: keynotec <filename>")
        sys.exit(1)

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
            keynote.metadata = metabase
            output.write(meta.read().format(**metabase))
        for plugin in keynote.plugins:
            output.write("\\input{{{plugin}}}".format(plugin=plugin))
        _generate_pagenumber(keynote, output)
        _generate_fullscreen(keynote, output)
        # print slides
        output.write('\\begin{document}')
        for type, data in keynote.slides:
            output.write(data)
        output.write('\\end{document}')
    print(" done.")

    print("Creating slides...", end='')
    error = _run_xelatex(texfile)
    print(" done.")

    print("Fixing references and effects...", end='')
    error |= _run_xelatex(texfile)
    print(" done.")

    print("Cleaning up...", end='')
    exts = ['aux', 'log', 'nav', 'out', 'snm', 'toc', 'vrb']
    exts = exts + ["tex"] if not error else exts
    for ext in exts:
        fname = '{}.{}'.format(name, ext)
        if os.access(fname, os.F_OK):
            os.unlink(fname)
    print("done.")

    if os.access('{}.pdf'.format(name), os.F_OK):
        print('{}.pdf'.format(name), "generated.")
