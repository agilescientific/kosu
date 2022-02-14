# Overview

## Main features

- There is one main command, `kosu`, which execute one of several sub-commands:
  - `build` &mdash; Build a course or courses. Reads the course's YAML file, finds and processes the notebooks in `prod`, compiles the course directory, and compresses everything into a ZIP file for course participants. This command has several options, see `kosu build --help`.
  - `clean` &mdash; Remove the build files associated with a course or courses.
  - `init` &mdash; Initialize a directory to start using kosu.
  - `publish` &mdash; Publish a course or courses to AWS.
  - `test` &mdash; Test that a course builds.
- You may only ever need to use `init` once, when you first start using `kosu`.
- There is a global control file, `.kosu.yaml`, which contains some parameters you will want to set and maintain.
- All of the other commands take either a single course name, or the `--all` flag, which applies the command to all the courses listed in `.kosu.yaml` under the `all` key.
- There is one control file per course, e.g. `geocomp.yaml`. This file contains the metadata for the course, including the curriculum and a list of its notebooks.
- There is one main, common environment file, `environment.yaml`. This contains packages to be installed for (i.e. common to)  all courses. A course's YAML control file lists any other packages to install for that class.


## Course project structure

The tool is designed to be used in a directory with the following structure:

```
foo
├── environment.yaml
├── example_course.yaml
├── images
│   └── agile_logo.png
├── .kosu.yaml
├── prod
│   ├── Interesting_notebook.ipynb
│   ├── Intro_to_Matplotlib.ipynb
│   ├── Intro_to_NumPy.ipynb
│   └── Intro_to_Python.ipynb
├── references
│   └── useful.pdf
├── scripts
│   └── example.py
└── templates
    └── README.md
```

## What happens during course compilation?

The course folder is built by `kosu build example_course` in the following way:

- A course folder is created in a (new if necessary) folder called `build`.
- A course README is built by placing the `curriculum` in the README template.
- The notebooks in the curriculum are processed as described below.
- Images required by the notebooks (detected automatically) are copied into an `images` folder.
- Scripts are copied into `master` and `notebooks` so they can be imported into any notebook.
- References are copied over into a `references` folder.
- We almost always import data from Amazon S3, making data files easy to detect. Accordingly, we check that data files mentioned in the notebooks are present in the S3 bucket.
- If some data files are to be included in the course repo, they are downloaded from the bucket and unzipped if necessary.
- A `conda` environment file is constructed from the various requirements in the global env file and the course control YAML file. (Dependencies are not yet detected from the notebooks.)
- The course folder is optionally zipped and optionally uploaded to S3.
- Build files are optionally cleaned up.

Jupyter Notebooks in the `prod` directory are processed in various ways:

- Two copies of the Notebooks are included in the course folder: one goes into the `master` folder, the other into `notebooks`. Students use the latter in the class.
- Cells with `exercise` tags are highlighted in green in the student notebooks.
- Cells with `info` tags are highlighted in blue in the student notebooks.
- Cells with `hide` tags are hidden in the student notebooks.
- Cell outputs are deleted in the student notebooks.

