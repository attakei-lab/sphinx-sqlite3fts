"""Core event handlers."""
from pathlib import Path
from typing import Optional

from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util.docutils import nodes

from . import models, services, utils


def setup_search_html(app: Sphinx, config: Config):
    """Update builder and configuration for using search.html with database."""
    if not app.config.sqlite3fts_use_search_html:
        return

    def _disable_search(app: Sphinx):
        app.builder.search = False

    def _generate_search_html(app: Sphinx):
        (Path(app.builder.outdir) / "searchindex.js").touch()
        app.builder.globalcontext.update(
            {
                "search_language_stop_words": "[]",
            }
        )
        return [("search", {}, "search.html")]

    static_path = utils.get_package_dir() / "static"
    config.html_static_path.insert(0, str(static_path))

    app.connect("builder-inited", _disable_search)
    app.connect("html-collect-pages", _generate_search_html)


def configure_database(app: Sphinx):
    """Connect database for project output."""
    db_path = Path(app.outdir) / "db.sqlite"
    if db_path.exists():
        db_path.unlink()
    models.initialize(db_path)


def register_document(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict,
    doctree: Optional[nodes.document] = None,
):
    """Register picked content into database."""
    if doctree is None:
        return
    if pagename in app.config.sqlite3fts_exclude_pages:
        return
    page = app.builder.get_target_uri(pagename)
    document, sections = services.parse_document(doctree, page)
    models.store_document(document, sections)


def save_database(app: Sphinx, err: Exception = None):
    """Save all data of database."""
    models.db_proxy.manual_commit()
