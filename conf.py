#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sphinx_rtd_theme


extensions = ['sphinx.ext.autodoc',  'sphinx.ext.coverage']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'pyMonet'
copyright = '2017, Przemyslaw Jan Pietrzak'
author = 'Przemyslaw Jan Pietrzak'
version = '0.12.0'
release = '0.12.0'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']

html_sidebars = {
    '**': [
        'relations.html',
        'searchbox.html',
    ]
}
htmlhelp_basename = 'pyMonetdoc'
latex_elements = {}

latex_documents = [
    (master_doc, 'pyMonet.tex', 'pyMonet Documentation', 'Przemyslaw Jan Pietrzak', 'manual'),
]

man_pages = [
    (master_doc, 'pymonet', 'pyMonet Documentation', [author], 1)
]

texinfo_documents = [
    (master_doc, 'pyMonet', 'pyMonet Documentation',
     author, 'pyMonet', 'One line description of project.',
     'Miscellaneous'),
]
