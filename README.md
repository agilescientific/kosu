# kōsu / コース

[![Tests](https://github.com/agilescientific/kosu/actions/workflows/tests.yml/badge.svg)](https://github.com/agilescientific/kosu/actions/workflows/tests.yml)
[![Build docs](https://github.com/agilescientific/kosu/actions/workflows/build-docs.yml/badge.svg)](https://github.com/agilescientific/kosu/actions/workflows/build-docs.yml)
[![PyPI version](https://img.shields.io/pypi/v/kosu.svg)](https://pypi.org/project/kosu/)
[![PyPI versions](https://img.shields.io/pypi/pyversions/kosu.svg)](https://pypi.org/project/kosu/)
[![PyPI license](https://img.shields.io/pypi/l/kosu.svg)](https://pypi.org/project/kosu/)

`kosu` is a command-line utility to help you build and maintain courses using Jupyter Notebooks.


## Installation

To install kosu:

    pip install kosu

Or if you want to upload to S3 later, use the `aws` option like so:

    pip install kosu[aws]

See [the documentation](https://code.agilescientific.com/kosu) for more information.


## Getting started

To set up a new collection of courses:

    mkdir mycourses
    cd mycourses
    kosu init

This will create several directories and files in the directory `mycourses`. You can run some of the other commands in this guide to see how they work.

The content of the course is controlled by `example-course.yaml`. Note that only `title` and `curriculum` are required fields. There is also a global control file, `.kosu.yaml`, which contains some parameters you will want to set and maintain.

To build the example course:

    kosu build example-course

This will create a ZIP file of the course content.

To add more courses using the same pool of content, add another YAML control file.


## Documentation

[Read the documentation](https://code.agilescientific.com/kosu) for more on using the tool, as well as for information about contributing to `kosu`, the licence, etc.
