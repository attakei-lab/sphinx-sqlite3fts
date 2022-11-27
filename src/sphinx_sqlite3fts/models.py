"""Management database schema."""
from pathlib import Path
from typing import Iterable

from playhouse import sqlite_ext

db_proxy = sqlite_ext.DatabaseProxy()


class Document(sqlite_ext.Model):
    """Document main model."""

    page = sqlite_ext.TextField(null=False, unique=True)
    title = sqlite_ext.TextField(null=False)

    class Meta:  # noqa: D106
        database = db_proxy


class Section(sqlite_ext.Model):
    """Section unit of document."""

    document = sqlite_ext.ForeignKeyField(Document)
    root = sqlite_ext.BooleanField(default=False, null=False)
    ref = sqlite_ext.TextField(null=False)
    title = sqlite_ext.TextField(null=False)
    body = sqlite_ext.TextField(null=False)

    class Meta:  # noqa: D106
        database = db_proxy


class Content(sqlite_ext.FTS5Model):
    """Searching model."""

    rowid = sqlite_ext.RowIDField()
    title = sqlite_ext.SearchField()
    body = sqlite_ext.SearchField()

    class Meta:  # noqa: D106
        database = db_proxy
        options = {"tokenize": "trigram"}


def store_document(document: Document, sections: Iterable[Section]):
    """Save document data into database."""
    document.save()
    for section in sections:
        section.document = document
        section.save()
        Content.insert(
            {
                Content.rowid: section.id,
                Content.title: section.title or document.title,
                Content.body: section.body,
            }
        ).execute()


def search_documents(keyword: str) -> Iterable[Section]:
    """Search documents from keyword by full-text-search."""
    return (
        Section.select()
        .join(Content, on=(Section.id == Content.rowid))
        .where(Content.match(keyword))
        .order_by(Content.bm25())
    )


def bind(db_path: Path):
    """Bind connection.

    This works only set db into proxy, not included creating tables.
    """
    db = sqlite_ext.SqliteExtDatabase(db_path)
    db_proxy.initialize(db)


def initialize(db_path: Path):
    """Bind connection and create tables."""
    bind(db_path)
    db_proxy.create_tables([Document, Section, Content])
