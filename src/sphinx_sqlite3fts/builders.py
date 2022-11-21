"""Management custom builders."""
from typing import Set

from sphinx.builders import Builder
from sphinx.util.docutils import nodes

from . import models


class SqliteBuilder(Builder):
    """Single database generation builder.

    This is custom builder to generate only SQLite database file
    """

    name = "sqlite"
    allow_parallel = True

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
        document.title = next(doctree.findall(nodes.title)).astext()
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
