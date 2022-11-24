===============
Getting started
===============

Requirements
============

* Python 3.7+

  * You can see requirement packages from ``pyproject.toml``.

* SQLite 3.34.0+

Installation
============

This is not published on PyPI.
If you want to try it, install from GitHub.

.. code-block:: console

   pip install git+https://github.com/attakei-lab/sphinx-sqlite3fts.git

Usage
=====

At first, configuration on ``conf.py`` of your documentation.

.. code-block:: python

   extensions = [
       "sphinx_sqlite3fts",
   ]

Try search by local database
----------------------------

You can build database by ``sqlite`` builder.

.. code-block:: console

   make sqlite
   sqlite3 _build/sqlite/db.sqlite

.. code-block:: sqlite3

   sqlite> SELECT * FROM documentindex MATCH "installation";

See :doc:`./database-spec`.
