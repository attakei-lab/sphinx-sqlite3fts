"""Test cases for section splitters."""
from pathlib import Path

import pytest
from sphinx.testing.restructuredtext import parse
from sphinx.testing.util import SphinxTestApp

from sphinx_sqlite3fts import models, services

RST_DIR = Path(__file__).parent / "rst"


@pytest.mark.sphinx("sqlite", testroot="default")
def test_single_section(app: SphinxTestApp):  # noqa
    rst_path = RST_DIR / "single-section.rst"
    doctree = parse(app, rst_path.read_text())
    document, sections = services.parse_document(doctree, rst_path.name)
    assert isinstance(document, models.Document)
    assert document.title == "Main title"
    assert len(sections) == 1
    assert sections[0].ref == "main-title"
    assert sections[0].title == ""
    assert sections[0].body == "This is first content."
    assert sections[0].root


@pytest.mark.sphinx("sqlite", testroot="default")
def test_sub_sections(app: SphinxTestApp):  # noqa
    rst_path = RST_DIR / "sub-sections.rst"
    doctree = parse(app, rst_path.read_text())
    document, sections = services.parse_document(doctree, rst_path.name)
    assert isinstance(document, models.Document)
    assert len(sections) == 2
    assert sections[1].title == "Sub section 1"
    assert not sections[1].root


@pytest.mark.sphinx("sqlite", testroot="default")
def test_multiple_sub_sections(app: SphinxTestApp):  # noqa
    rst_path = RST_DIR / "multiple-sub-sections.rst"
    doctree = parse(app, rst_path.read_text())
    document, sections = services.parse_document(doctree, rst_path.name)
    assert isinstance(document, models.Document)
    assert len(sections) == 3
