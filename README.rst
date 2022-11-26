=================
sphinx-sqlite3fts
=================

Sphinx new search page using SQL.js and SQLite database included FTS extension.

.. image:: https://img.shields.io/pypi/v/sphinx-sqlite3fts.svg
    :target: https://pypi.org/project/sphinx-sqlite3fts/

.. image:: https://github.com/attakei-lab/sphinx-sqlite3fts/actions/workflows/main.yml/badge.svg?branch=main
   :alt: Run CI
   :target: https://github.com/attakei-lab/sphinx-sqlite3fts/actions/workflows/main.yml

.. image:: https://readthedocs.org/projects/sphinx-sqlite3fts/badge/?version=latest
    :target: https://sphinx-sqlite3fts.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. note:: This is experimental library

Overview
========

This is sphinx extension to provide search component with full-text search database.

When ``sphinx-build`` runs with this extension, builder generate these components.

* SQLite database with FTS extension
* Records of all documents
* Search page HTML with sql.js

This will be useful when you want to embed strong full-text search with keeping static-site structure.

Installation
============

This is not published on PyPI.

.. code-block:: console

   pip install git+https://github.com/attakei-lab/sphinx-sqlite3fts.git

Usage
=====

1. Register extension into your ``conf.py`` and configure it.

.. code-block:: python

   extensions = [
       #
       # Other extensions
       #
       "sphinx_sqlite3fts",  # Add it
   ]

2. Run builder (html-based builder only).

.. code-block:: console

   sphinx-build -M html source build

3. To try it in local, use ``http.server`` module.

.. code-block:: console

   python -m http.server -d build

  Please access http://localhost:8000/search.html
