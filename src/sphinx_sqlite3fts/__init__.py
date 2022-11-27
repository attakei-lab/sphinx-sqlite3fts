"""Sphinx document searcher using SQLite3."""
from sphinx.application import Sphinx

from . import builders, events

__version__ = "0.1.0"


def setup(app: Sphinx):
    """Entrypoint as Sphinx extension."""
    app.add_config_value("sqlite3fts_exclude_pages", [], "env")
    app.add_config_value("sqlite3fts_use_search_html", False, "env")
    app.add_builder(builders.SqliteBuilder)
    app.connect("config-inited", events.setup_search_html)
    app.connect("builder-inited", events.configure_database)
    app.connect("html-page-context", events.register_document)
    app.connect("build-finished", events.save_database)
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
    }
