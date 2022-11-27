=============
Configuration
=============

.. confval:: sqlite3fts_exclude_pages

   :Type: ``List[str]``
   :Default: ``[]``
   :Example: ``["index", "404"]``

   List of documents that are excluded for target of register database.
   This should be used when some documents need not be searched.

   Value must be **docname**, not filename.
   If you want to exclude ``index.rst``, you should set ``index``.

.. confval:: sqlite3fts_use_search_html

   :Type: ``bool``
   :Default: ``False``
   :Example: ``True``

   Use custom search page.

   If you set ``True`` for this, ``sphinx-sqlite3fts`` does these.

   * Override JavaScript file for search.
   * Change style to display search results.
