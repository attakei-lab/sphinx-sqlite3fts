======================
Database specification
======================

This is writing about specification of generated database.

Base
====

Using SQLite and FTS5 extension.
Details are described in `SQLite website <https://www.sqlite.org/fts5.html>`_.

``sphinx-sqlite3fts`` run these strategy.

* Use ``trigram`` tokenizer to search Japanese text (not work with ``unicode61``).
* Split document table and searching virtual table (document has ``page`` that is not target of search).

Tables
======

``sphinx-sqlite3fts`` use peewee to manage database schemas.

document table
--------------

This table contains all of property for refer to documents.

document-fts table
------------------

This table is registered only targets of full-text searching.
Currently, this contains title and body of documents.

``body`` is plain text to pick all text contents from doctree.

Relation
--------

``document-fts.rowid`` is as foreign key to ``document.id``.
You can use ``JOIN`` statement two tables.
