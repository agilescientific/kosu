# Using `kosu`

`kosu` has 6 commands:

- **`help`** &mdash; Get brief help.
- **`init`** &mdash; Start a new set of courses.
- **`build`** &mdash; Compile and zip a course.
- **`clean`** &mdash; Delete old build files.
- **`test`** &mdash; Test that a course builds without creating any artifacts.
- **`publish`** &mdash; Build and publish a course to the cloud.

These are run like `kosu build` etc. Each command is fully explained below.


## Usage of `help`

To see high-level help:

    kosu --help


## Usage of `init`

**You will likely only ever need this command once, the very first time you start using kosu.**

Initializes a new course (or courses) project. This command creates the cirectory structure you'll need. Make sure to run it in a new folder:

    mkdir mycourses
    cd mycourse
    kosu init

You can build the example project this creates:

kosu build example-course

This will create a ZIP file of the course content.

To add more courses using the same pool of content, add another YAML control file. 


## Usage of `build`

Run the `kosu` command like this to build a course called `example-course`:

    kosu build example-course

You can build any course for which a YAML file exists. So the command above will compile the course specified by `example-course.yaml`.

In addition, you can pass the following options:

- **`--clean` / `--no-clean`** &mdash; Whether to delete the build files. Default: `clean`.
- **`--zip` / `--no-zip`** &mdash; Whether to **create** the zip file for the course repo. Default: `zip`.
- **`--upload` / `--no-upload`** &mdash; Whether to **upload** the zip file to `geocomp.s3.amazonaws.com`. Default: `no-upload`. Note that this requires AWS credentials to be set up on your machine.
- **`--clobber` / `--no-clobber`** &mdash; Whether to silently overwrite existing ZIP file and/or build directory. If `no-clobber`, the CLI will prompt you to overwrite or not. Default: `no-clobber`.
- **`--all`** &mdash; Process all of the courses listed in `.kosu.yaml`, if listed; if there is no such list then all of the courses in the source directory are processed.


## Usage of `clean`

Cleans the build files for a course, with optional `--all` flag. I.e. everything in `build` and its ZIP file.

    kosu clean example-course


## Usage of `test`

Shortcut for `build --clobber --clean --no-zip --no-upload`, with optional `--all` flag, and with an extra option to build an environment file for `conda`.

Tests that a specific course builds, leaving no sawdust, or use the `--all` option to test all courses in `all.yaml`. This command builds a course, does not make a ZIP, does not uplad anything, and removes the build folder. (To keep the build folder or make a zip, use the `build` command with the appropriate options, see above.) Here's how to test the machine learning course:

    kosu test example-course

There is an option `--environment` that will also generate an environment file called `environment-all.yml`. (This is used for automated testing on GitHub.)

In general, if a course does not build, the script will throw an error. It does not try to deal with or interpret the error or explain what's wrong.


## Usage of `publish`

Shortcut for `build --clobber --upload --clean`, with optional `--all` flag.

Publish a course, or those listed in `all.yaml`. The ZIP file(s) will be uploaded to AWS. For example, to publish all the courses:

    kosu publish --all
