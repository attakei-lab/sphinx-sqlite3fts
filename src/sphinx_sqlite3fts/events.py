"""Core event handlers."""
from pathlib import Path

from sphinx.application import Sphinx

from . import models


def configure_database(app: Sphinx):
    """Connect database for project output."""
    db_path = Path(app.outdir) / "db.sqlite"
    if db_path.exists():
        db_path.unlink()
    models.initialize(db_path)


def save_database(app: Sphinx, err: Exception = None):
    """Save all data of database."""
    models.db_proxy.manual_commit()
