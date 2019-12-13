# KeynoteC

A simple DSL to create keynote presentations using LaTeX and Beamer.

## Usage

At this state, **KeynoteC** is usable as a Python executable module, or as
an application. Install it with `python3 setup.py install` (you might need
superuser priviledges to install in system wide), and execute the module as
`python3 -m keynotec <filename>`, or the application `keynotec <filename>`, to
compile the keynote file into a PDF presentation.

## Syntax

The file [keynote.key](keynote.key) file as an example of everything
that is currently working, and serves as an example.

For a more thorough explanation of the syntax you might want to take a look
at [docs/syntax.md](docs/syntax.md).

## Dependencies

**XeLaTeX** is used to generate the PDF output file. Also, the following LaTeX
packages are required:

* beamer
* inputenc
* fontspec
* enumitem
* calc
* datetime
* babel
* listings

## Installation

You can instal KeynoteC trough Python `pip`:

```
% python3 -m pip install keynotec
```

On most Linux distribution you would use a TexLive distribution and it should
be enough, apart from some missing packages. Use your Linux distrubution
package manager to install them.

On macOS, disk space is a premium (as is anything with the cost of a Mac), so
if, like me, you bought just barely enough disk space, and cannot upgrade it
since it is soldered on the logic board, you should NOT use a full fledged
TexLive distribution. Instead you should use
[BasicTex](https://www.tug.org/mactex/morepackages.html), that will eat just
a hundred megs of your precious disk, and then use its package manager to
install the missing packages (with sudo):

```
% sudo tlmgr update —self
% sudo tlmgr install enumitem datetime fmtcount  
```

The example above install the really minimum required, you can use
`tlmgr install` if you find that you need anything else.


## Code Quality

It works. It does what I need. I built the first version in about 24h. It was
much less than that in work hours. And the code shows it. Live with that. I do.

To aid in its development, report any issue you have or enhancement in the
project's [Github repository](https://github.com/rafasgj/keynotec).

Thank you.
