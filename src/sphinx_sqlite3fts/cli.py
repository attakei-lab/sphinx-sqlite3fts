"""CLI entrypoint."""
import sys
from pathlib import Path

try:
    import click
except ImportError:
    sys.stderr.write("CLI command need Click.\n")
    sys.stderr.write("Please install by `pip install 'sphinx-sqlite3fts[cli]'`.\n")
    sys.exit(1)

from . import models


@click.command
@click.argument(
    "db",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, resolve_path=True, path_type=Path
    ),
)
@click.argument("keyword")
def main(db: Path, keyword: str):
    """Search documents by keyword.

    Results are formated by:
    - docname
    - [TAB]document title
    - [BLANK]
    """
    models.bind(db)
    for section in models.search_documents(keyword):
        click.secho(section.document.page, fg="green")
        if section.title:
            click.echo(f"\t{section.document.title} / {section.title}")
        else:
            click.echo(f"\t{section.document.title}")
        click.echo("")


if __name__ == "__main__":
    main()
