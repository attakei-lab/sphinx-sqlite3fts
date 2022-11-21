"""Test cases for custom builders."""
import sqlite3
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("sqlite", testroot="default")
def test___work_builder(app: SphinxTestApp, status, warning):  # noqa
    app.build()
    db_path = Path(app.outdir) / "db.sqlite"
    assert db_path.exists()
    conn = sqlite3.connect(db_path)
    assert len(conn.execute("SELECT * FROM document").fetchall()) > 0
