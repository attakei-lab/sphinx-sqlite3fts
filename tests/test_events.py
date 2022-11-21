"""Test cases for result of events."""
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html", testroot="default")
def test___work_builder(app: SphinxTestApp, status, warning):  # noqa
    app.build()
    db_path = Path(app.outdir) / "db.sqlite"
    assert db_path.exists()
