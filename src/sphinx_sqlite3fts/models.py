"""Management database schema."""
from pathlib import Path
from typing import Iterable

from playhouse import sqlite_ext

db_proxy = sqlite_ext.DatabaseProxy()


class Document(sqlite_ext.Model):
    """Document main model."""

    page = sqlite_ext.TextField(null=False, unique=True)
    title = sqlite_ext.TextField(null=False)
    body = sqlite_ext.TextField(null=False)

    class Meta:  # noqa: D106
        database = db_proxy


class DocumentFTS(sqlite_ext.FTS5Model):
    """Searching model."""

    rowid = sqlite_ext.RowIDField()
    title = sqlite_ext.SearchField()
    body = sqlite_ext.SearchField()

    class Meta:  # noqa: D106
        database = db_proxy
        options = {"tokenize": "trigram"}


def store_document(document: Document):
    """Save document data into database."""
    document.save()
    DocumentFTS.insert(
        {
            DocumentFTS.rowid: document.id,
            DocumentFTS.title: document.title,
            DocumentFTS.body: document.body,
        }
    ).execute()


def search_documents(keyword: str) -> Iterable[Document]:
    """Search documents from keyword by full-text-search."""
    return (
        Document.select()
        .join(DocumentFTS, on=(Document.id == DocumentFTS.rowid))
        .where(DocumentFTS.match(keyword))
        .order_by(DocumentFTS.bm25())
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
    db_proxy.create_tables([Document, DocumentFTS])
