# KeynoteC

A simple DSL to create keynote presentations using LaTeX and Beamer.

## Usage

At this state, **KeynoteC** is usable as a Python executable module. Run
it with `python -m keynotec <filename.key>` to compile the keynote file
into a PDF presentation.

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

## Code Quality

It works. It does what I need. I built the first version in about 24h. It was
much less than that in work hours. And the code shows it. Live with that. I do.

To aid in its development, report any issue you have or enhancement in the
project's [Github repository](https://github.com/rafasgj/keynotec).

Thank you.
