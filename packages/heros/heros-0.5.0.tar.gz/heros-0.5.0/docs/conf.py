# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'HEROS'
copyright = '2025, Thomas Niederprüm'
author = 'Thomas Niederprüm'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# -- General configuration ---------------------------------------------------
extensions = [
    # 'sphinx.ext.autodoc',     # Include docstrings in the documentation
    'autoapi.extension',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',    # Support for Google and NumPy style docstrings
    'sphinx.ext.viewcode',    # Add links to source code
    'sphinx.ext.todo',  # Enable todo lists
    'sphinx_autodoc_typehints',  # Handle type hints in documentation
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_theme_options = {
    "light_logo": "heros_logo.svg",
    "dark_logo": "heros_logo.svg",
    "sidebar_hide_name": False,
}

# Autodoc settings
autoclass_content = "both"
# -- AutoAPI configuration ---------------------------------------------------
autoapi_type = 'python'
autoapi_dirs = ['../src']  # Path to your source code
autoapi_add_toctree_entry = True  # Avoid duplicate toctree entries
autoapi_keep_files = False  # Keep intermediate reStructuredText files
# todo conf
todo_include_todos = True
