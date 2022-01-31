# kōsu / コース

[![PyPI status](https://img.shields.io/pypi/status/kosu.svg)](https://pypi.org/project/kosu/)
[![PyPI versions](https://img.shields.io/pypi/pyversions/kosu.svg)](https://pypi.org/project/kosu/)
[![PyPI license](https://img.shields.io/pypi/l/kosu.svg)](https://pypi.org/project/kosu/)

Build and maintain courses using Jupyter Notebooks.

The main features:

- There is one main command, `kosu`, which execute one of several sub-commands:
  - `build` &mdash; Build a course or courses. This command has several options, see `kosu build --help`.
  - `clean` &mdash; Remove the build files associated with a course or courses.
  - `init` &mdash; Initialize a directory to start using kosu.
  - `publish` &mdash; Publish a course or courses to AWS.
  - `test` &mdash; Test that a course builds.
- You may only ever need to use `init` once, when you first start using `kosu`.
- There is a global control file, `.kosu.yaml`, which contains some parameters you will want to set and maintain.
- All of the other commands take either a single course name, or the `--all` flag, which applies the command to all the courses listed in `.kosu.yaml` under the `all` key.
- There is one control file per course, e.g. `geocomp.yaml`. This file contains the metadata for the course, including the curriculum and a list of its notebooks.
- There is one main, common environment file, `environment.yaml`. This contains packages to be installed for (i.e. common to)  all courses. A course's YAML control file lists any other packages to install for that class.


## Installation

To install kosu:

    pip install kosu


## Getting started

To set up a new collection of courses:

    mkdir mycourses
    cd mycourses
    kosu init

This will create several directories and files in the directory `mycourses`. You can run some of the other commands in this guide to see how they work.


## Usage

To see high-level help:

    kosu --help


### Usage of `build`

Run the `kosu` command like this to build a course called `example-course`:

    kosu build example-course

You can build any course for which a YAML file exists. So the command above will compile the course specified by `example-course.yaml`.

All of the commands can take the option `--all`. This will apply the command to all of the courses listed in `all.yaml`. In this case, don't pass any individual course name.

In addition, you can pass the following options:

- **`--clean` / `--no-clean`** &mdash; Whether to delete the build files. Default: `clean`.
- **`--zip` / `--no-zip`** &mdash; Whether to **create** the zip file for the course repo. Default: `zip`.
- **`--upload` / `--no-upload`** &mdash; Whether to **upload** the zip file to `geocomp.s3.amazonaws.com`. Default: `no-upload`. Note that this requires AWS credentials to be set up on your machine.
- **`--clobber` / `--no-clobber`** &mdash; Whether to silently overwrite existing ZIP file and/or build directory. If `no-clobber`, the CLI will prompt you to overwrite or not. Default: `no-clobber`.


### Usage of `clean`

Cleans the build files for a course. I.e. everything in `build` and its ZIP file.

    kosu clean example-course


### Usage of `publish`

Publish a course, or those listed in `all.yaml`. The ZIP file(s) will be uploaded to AWS. For example, to publish all the courses:

    kosu publish --all


### Usage of `test`

Tests that a specific course builds, leaving no sawdust, or use the `--all` option to test all courses in `all.yaml`. This command builds a course, does not make a ZIP, does not uplad anything, and removes the build folder. (To keep the build folder or make a zip, use the `build` command with the appropriate options, see above.) Here's how to test the machine learning course:

    kosu test example-course

There is an option `--environment` that will also generate an environment file called `environment-all.yml`. (This is used for automated testing on GitHub.)

In general, if a course does not build, the script will throw an error. It does not try to deal with or interpret the error or explain what's wrong.


## Example control file

See `example-course.yaml`. Note that only `title` and `curriculum` are required fields.
