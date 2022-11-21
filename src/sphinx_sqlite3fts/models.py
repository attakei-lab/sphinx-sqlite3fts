"""Management database schema."""
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
