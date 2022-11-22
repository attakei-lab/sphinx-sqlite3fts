"""Core event handlers."""
from pathlib import Path
from typing import Optional

from sphinx.application import Sphinx
from sphinx.util.docutils import nodes

from . import models, services


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
    title, body = services.parse_document(doctree)
    document = models.Document(page=page, title=title, body=body)
    models.store_document(document)


def save_database(app: Sphinx, err: Exception = None):
    """Save all data of database."""
    models.db_proxy.manual_commit()
