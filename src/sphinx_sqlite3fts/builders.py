"""Management custom builders."""
from pathlib import Path
from typing import Set

from peewee import SqliteDatabase
from sphinx.builders import Builder
from sphinx.util.docutils import nodes

from . import models


class SqliteBuilder(Builder):
    """Single database generation builder.

    This is custom builder to generate only SQLite database file
    """

    name = "sqlite"
    allow_parallel = True

    def init(self):
        """At first, bind database into db-proxy and create tables.

        If database is exists, remove it for clean up.
        """
        db_path = Path(self.outdir) / "db.sqlite"
        if db_path.exists():
            db_path.unlink()
        db = SqliteDatabase(db_path)
        models.db_proxy.initialize(db)
        models.db_proxy.create_tables([models.Document, models.DocumentFTS])

    def get_target_uri(self, docname: str, typ: str = None) -> str:  # noqa: D102
        return docname

    def get_outdated_docs(self) -> str:  # noqa: D102
        return "db.sqlite"

    def prepare_writing(self, docnames: Set[str]) -> None:  # noqa: D102
        pass

    def write_doc(self, docname: str, doctree: nodes.document) -> None:
        """Register content of document into database.

        This method only insert into db, does not write file.
        """
        document = models.Document(page=docname)
        titles = doctree.traverse(nodes.title)
        document.title = titles[0].astext()
        contents = []
        picked_title = False
        for section in doctree.children:
            for node in section.children:
                if isinstance(node, nodes.title) and not picked_title:
                    picked_title = True
                    continue
                contents.append(node.astext())
        document.body = "\n".join(contents)
        models.store_document(document)

    def handle_finish(self):
        """Save database."""
        models.db_proxy.manual_commit()
