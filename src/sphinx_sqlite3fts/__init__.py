"""Sphinx document searcher using SQLite3."""
from sphinx.application import Sphinx
from sphinx.util import logging

from . import builders, events

__version__ = "0.1.2"

logger = logging.getLogger(__name__)


def setup(app: Sphinx):
    """Entrypoint as Sphinx extension."""
    logger.warning(
        f"{__name__} is archived on {__version__}. Please use 'atsphinx-sqlite3fts'."
    )
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
