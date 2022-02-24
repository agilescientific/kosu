# Configuration file for Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------
project = 'kosu'
copyright = '2022, Agile Scientific'
author = 'Agile Scientific'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'myst_parser',
    'sphinx.ext.coverage', 
]
 
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'notebooks']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# https://sphinx-themes.org/sample-sites/furo/
html_theme = 'furo'

html_theme_options = {
    "sidebar_hide_name": True,
    "footer_icons": [
        {
            "name": "Agile",
            "url": "https://code.agilescientific.com",
            "html": """
                <svg width="200" height="200" version="1.1" viewBox="0 0 187.5 187.5" xmlns="http://www.w3.org/2000/svg">
                <g transform="matrix(3.94 -1.28 1.28 3.94 -906.1 -3676)" style="color-rendering:auto;color:#000000;fill:#14ca29;image-rendering:auto;isolation:auto;mix-blend-mode:normal;shape-rendering:auto;solid-color:#000000;stroke-width:1px;text-decoration-color:#000000;text-decoration-line:none;text-decoration-style:solid;text-indent:0;text-transform:none;white-space:normal">
                <path d="m-46.98 936.1q3.515-1.622 6.705-3.244t5.083-2.379 3.028-0.757q1.893 0 3.244 1.298 1.406 1.244 1.406 3.136 0 1.081-0.7029 2.271-0.6489 1.136-1.406 1.46-6.975 2.758-15.36 4.001 1.514 1.406 3.731 3.731t2.325 2.487q0.8111 1.136 2.271 2.812 1.46 1.676 2.001 2.65 0.5948 0.9192 0.5948 2.271 0 1.73-1.298 3.028t-3.352 1.298q-2.055 0-4.65-3.19-2.541-3.19-6.597-11.46-4.109 7.462-5.515 9.841t-2.704 3.623q-1.298 1.19-2.974 1.19-2.001 0-3.352-1.352-1.298-1.406-1.298-2.974 0-1.46 0.5407-2.217 4.975-6.759 10.38-11.73-4.542-0.7029-8.111-1.568t-7.57-2.541q-0.6489-0.3244-1.298-1.46-0.5948-1.19-0.5948-2.163 0-1.893 1.352-3.136 1.406-1.298 3.19-1.298 1.298 0 3.244 0.8111 1.947 0.757 4.921 2.271 3.028 1.46 6.867 3.298-0.7029-3.407-1.19-7.786-0.4326-4.434-0.4326-6.056 0-2.001 1.244-3.407 1.298-1.46 3.298-1.46 1.947 0 3.19 1.46 1.298 1.406 1.298 3.785 0 0.6489-0.2163 2.595-0.1622 1.893-0.5407 4.65-0.3244 2.704-0.757 6.218z" style="fill:#14ca29"/>
                </g>
                </svg>
            """,
            "class": "",
        },
    ],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    'custom.css',
]

# Branding.
html_favicon = '_static/favicon.ico'
html_logo = '_static/kosu_logo.png'
