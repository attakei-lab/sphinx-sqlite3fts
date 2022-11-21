"""Application services."""
from typing import Tuple

from sphinx.util.docutils import nodes


def parse_document(doctree: nodes.document) -> Tuple[str, str]:
    """Pick title and body from doctree."""
    title = next(doctree.findall(nodes.title)).astext()
    contents = []
    picked_title = False
    for section in doctree.children:
        for node in section.children:
            if isinstance(node, nodes.title) and not picked_title:
                picked_title = True
                continue
            contents.append(node.astext())
    return title, "\n".join(contents)
