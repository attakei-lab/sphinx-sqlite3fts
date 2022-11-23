"""Sphinx document searcher using SQLite3."""
from sphinx.application import Sphinx

from . import events

__version__ = "0.0.2"


def setup(app: Sphinx):
    """Entrypoint as Sphinx extension."""
    from .builders import SqliteBuilder

    # TODO: Add documentation
    app.add_config_value("sqlite3fts_exclude_pages", [], "env")
    app.add_builder(SqliteBuilder)
    app.connect("builder-inited", events.configure_database)
    app.connect("html-page-context", events.register_document)
    app.connect("build-finished", events.save_database)
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
    }
