# KeynoteC

A simple DSL to create keynote presentations using LaTeX and Beamer.

## Usage

At this state, it is barely usable, run it on its own directory,
`python keynotec.py <filename.key>` and then execute `make -C template` to
compile the keynote to `template/out.pdf`.

> Yes, I will fix it soon, but I need this repository up sooner than I wanted.

## Syntax

For now, use the [keynote.key](keynote.key) file as an example of everything
that is already working.

## Dependencies

The following LaTeX packages are required:

* beamer
* inputenc
* fontspec
* enumitem
* calc
* datetime
* babel
* listings
