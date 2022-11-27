"""Application services."""
from typing import List, Tuple

from sphinx.util.docutils import nodes

from . import models


def parse_document(
    doctree: nodes.document,
    pagename: str,
) -> Tuple[models.Document, List[models.Section]]:
    """Pick title and body from doctree."""
    # Parse
    root = next(doctree.findall(nodes.section))
    sections = []
    contents = []
    for node in root.children:
        if isinstance(node, nodes.title):
            continue
        elif isinstance(node, nodes.section):
            sections.append(parse_section(node))
            continue
        contents.append(node.astext())

    root_section = models.Section(
        ref=root.attributes["ids"][0],
        title="",
        body="\n".join(contents),
        root=True,
    )
    document = models.Document(
        page=pagename,
        title=next(doctree.findall(nodes.title)).astext(),
    )
    return document, [root_section] + sections


def parse_section(
    root: nodes.section,
) -> Tuple[models.Document, List[models.Section]]:
    """Pick title and body from section of doctree."""
    # Parse
    contents = []
    for node in root.children:
        if isinstance(node, nodes.title):
            continue
        contents.append(node.astext())

    return models.Section(
        ref=root.attributes["ids"][0],
        body="\n".join(contents),
        title=next(root.findall(nodes.title)).astext(),
    )
