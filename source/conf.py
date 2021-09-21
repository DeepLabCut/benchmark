# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import pydata_sphinx_theme


# -- Project information -----------------------------------------------------

project = "DeepLabCut Benchmark"
copyright = "2021, DeepLabCut Developers"
author = "DeepLabCut Developers"
html_title = "DeepLabCut benchmark"
html_short_title = "DLC Benchmark"


# The full version, including alpha/beta/rc tags
release = "0.0.1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["navbar-icon-links"],
    "page_sidebar_items": [],
    "icon_links": [
        {
            "name": "Github",
            "url": "https://github.com/deeplabcut/benchmark",
            "icon": "fab fa-github",
        },
        {
            "name": "Twitter",
            "url": "https://twitter.com/DeepLabCut",
            "icon": "fab fa-twitter",
        },
    ],
    "external_links": [
        {"name": "DeepLabCut", "url": "https://deeplabcut.org/"},
    ],
    "show_prev_next": False,
}

html_logo = '_static/img/dlc-logo-violet.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_sidebars = {"**": []}