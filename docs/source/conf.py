# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


import os, sys

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "RAPI"
copyright = "2023, Czech Radio"
author = "Czech Radio"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [    
    "myst_parser",
    "nbsphinx",
    "sphinx.ext.viewcode",
    # "autoapi.extension",
]

suppress_warnings = [
    'nbsphinx', # PandocMissing ... https://nbsphinx.readthedocs.io/en/0.9.3/configuration.html#suppress_warnings
]

# autoapi_dirs = ["../../src"]

templates_path = ["_templates"]
exclude_patterns = ["_static", "_build",]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_logo = "_static/CRo-Czech_Radio-H-RGB.png"