#!/usr/bin/env python3
"""Setup information for KeynoteC package."""

from setuptools import setup, find_packages


def _read(fname):
    import os.path
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="KeynoteC",
    version="0.2.2",
    packages=find_packages(),
    platforms=['any'],
    # scripts=['keynotec'],
    package_data={
        'keynotec': ['keynotec/resources'],
    },

    author="Rafael Guterres Jeffman",
    author_email="rafasgj@gmail.com",
    description="KeynoteC is a DSL processor for creting keynotes with Latex.",
    long_description=_read('README.md'),
    long_description_content_type='text/markdown',
    license="GPLv3",
    keywords="DSL keynote Latex Beamer slides",
    url="https://github.com/rafasgj/keynotec",
    entry_points={
        'console_scripts': ['keynotec = keynotec:run']
    },
    include_package_data=True,
)
