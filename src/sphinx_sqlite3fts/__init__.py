"""Sphinx document searcher using SQLite3."""
from sphinx.application import Sphinx

__version__ = "0.0.1"


def setup(app: Sphinx):
    """Entrypoint as Sphinx extension."""
    from .builders import SqliteBuilder

    app.add_builder(SqliteBuilder)
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
    }
