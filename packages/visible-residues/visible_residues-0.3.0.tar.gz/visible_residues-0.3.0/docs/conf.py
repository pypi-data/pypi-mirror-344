import visible_residues

## General

project = 'Visible Residues'
copyright = '2025, Kale Kundert'
version = visible_residues.__version__
release = visible_residues.__version__

master_doc = 'index'
source_suffix = '.rst'
templates_path = ['_templates']
exclude_patterns = ['_build']
html_static_path = ['_static']
default_role = 'any'
trim_footnote_reference_space = True
nitpicky = True

## Extensions

extensions = [
        'autoclasstoc',
        'myst_parser',
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary',
        'sphinx.ext.viewcode',
        'sphinx.ext.intersphinx',
        'sphinx.ext.napoleon',
        'sphinx_rtd_theme',
]
intersphinx_mapping = {
        'python': ('https://docs.python.org/3', None),
}
autosummary_generate = True
autodoc_default_options = {
        'exclude-members': '__dict__,__weakref__,__module__,__annotations__',
}
html_theme = 'sphinx_rtd_theme'
pygments_style = 'sphinx'

