#!/usr/bin/env python3
# -*- coding: utf-8 -*-

extensions = ['sphinx.ext.autodoc',  'sphinx.ext.coverage']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'pyMonet'
copyright = '2017, Przemyslaw Jan Pietrzak'
author = 'Przemyslaw Jan Pietrzak'
version = '0.7.0'
release = '0.7.0'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
hey produce nothing.
todo_include_todos = False
html_theme = 'alabaster'
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
    (master_doc, 'pyMonet.tex', 'pyMonet Documentation',
     'Przemyslaw Jan Pietrzak', 'manual'),
]

man_pages = [
    (master_doc, 'pymonet', 'pyMonet Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'pyMonet', 'pyMonet Documentation',
     author, 'pyMonet', 'One line description of project.',
     'Miscellaneous'),
]



