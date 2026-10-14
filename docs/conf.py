"""Sphinx configuration for the installed public package."""

from importlib.metadata import version as distribution_version

project = "python-traceprint"
author = "Lucas Lopez"
copyright = "2026, Lucas Lopez"
release = distribution_version("python-traceprint")
version = release
extensions = ["sphinx.ext.autodoc"]
autodoc_member_order = "bysource"
autodoc_typehints = "signature"
autoclass_content = "both"
exclude_patterns = ["_build"]
html_theme = "alabaster"
html_title = f"{project} {release}"
