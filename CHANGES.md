# Changelog

## 0.1.5 &mdash; 18 May 2022

- Improved the appearance of feedback messages, and added emojis.
- Improved the rendering of `info` and `exercise` boxes in notebooks.
- Implemented various CI and development updates.


## 0.1.4 &mdash; 24 Feb 2022

- Added more parameters to `.kosu.yaml` so you can change which folders assets are both kept in and copied to in the build.
- Added a missing file preventing new projects from being initialized with `init`.
- Added a check that the directory is empty before proceeding with `init`.
- Improved the documentation.


## 0.1.3 &mdash; 14 Feb 2022

- Documentation synced with software.
- Removed Boto3 as dependency (was breaking CI anyway).
- Added support for older versions of Python.


## 0.1.2 &mdash; Feb 2022

- Added color to the terminal messages, fixing [#7](https://github.com/agilescientific/kosu/issues/7). Thank you to [@Arunodhai](https://github.com/Arunodhai) for this enhancement.


## 0.1.1 &mdash; 31 Jan 2022

- More tests, and demo project now builds.


## 0.1.0 &mdash; 31 Jan 2022

- Initial release


## Origin story

`kosu` was built around a Jupyter Notebook processing script we made in about 2015 to support Agile's Python classes. Our hands-on process got out of hand as we added more courses and variants to our portfolio. We started this tool in November 2021 and released it in January 2022; it represents an attempt to make the courses easier to define and manage.
