import sys
from pathlib import Path

sys.path.insert(
    0, Path.cwd().parent.parent / "src" / "hoa_insights_surpriseaz"
)  # Source code dir relative to this file

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "HOA_INSIGHTS_SURPRISEAZ"
copyright = "2025, TASCS"
author = "TASCS"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.duration",
    "sphinx.ext.autosummary",
    "sphinx_readme",

]

html_context = {
   'display_github': True,
   'github_user': 'TASCer',
   'github_repo': 'hoa_insights_surpriseaz',
}

html_baseurl = "https://github.com/TASCer/hoa_insights_surpriseaz/"

readme_src_files = "README.md"

readme_docs_url_type = "html"


autodoc_inherit_docstrings = True  # If no docstring, inherit from base class
autosummary_generate = True  # Turn on sphinx.ext.autosummary

templates_path: list[str] = ["_templates"]
exclude_patterns: list[str] = ["_build", "_templates", ".DS_Store", "my_secrets.rst"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path: list[str] = ["_static"]
