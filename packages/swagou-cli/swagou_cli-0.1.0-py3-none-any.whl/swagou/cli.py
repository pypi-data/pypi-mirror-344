"""Command-line interface for swagou."""

import sys
from typing import List, Optional

import typer
from rich.console import Console

from swagou.filter import filter_openapi_schema

app = typer.Typer(
    name="swagou",
    help="Swagger Opinionated utilities for filtering OpenAPI specifications",
    add_completion=False,
)
console = Console()


@app.command("filter")
def filter_command(
    input_source: str = typer.Option(
        ...,
        "--input",
        "-i",
        help="Input source: URL to the schema or path to a file",
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (default: stdout)",
    ),
    get: List[str] = typer.Option(
        [],
        "--get",
        "-g",
        help="Filter GET endpoints by path pattern",
    ),
    post: List[str] = typer.Option(
        [],
        "--post",
        "-p",
        help="Filter POST endpoints by path pattern",
    ),
    patch: List[str] = typer.Option(
        [],
        "--patch",
        "-u",
        help="Filter PATCH endpoints by path pattern",
    ),
    delete: List[str] = typer.Option(
        [],
        "--delete",
        "-d",
        help="Filter DELETE endpoints by path pattern",
    ),
    all_methods: List[str] = typer.Option(
        [],
        "--all",
        help="Filter all HTTP methods for endpoints by path pattern",
    ),
    header: Optional[List[str]] = typer.Option(
        None,
        "--header",
        help="HTTP header to include in requests (format: 'Name: Value')",
    ),
    cookie: Optional[List[str]] = typer.Option(
        None,
        "--cookie",
        help="Cookie to include in requests (format: 'Name: Value')",
    ),
    tags: Optional[List[str]] = typer.Option(
        None,
        "--tags",
        "-t",
        help="Filter by tags",
    ),
):
    """
    Filter OpenAPI/Swagger documentation to include only specified endpoints.

    Examples:
        swagou filter --input swagger.yaml --get /api/posts/ --get /api/posts/{slug}/
        swagou filter --input https://example.com/api/schema/ --header="Authorization: Token abc123" --all /api/users/*
    """
    try:
        result = filter_openapi_schema(
            input_source=input_source,
            get_paths=get,
            post_paths=post,
            patch_paths=patch,
            delete_paths=delete,
            all_paths=all_methods,
            headers=header,
            cookies=cookie,
            tags=tags,
        )

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            console.print(f"[green]Filtered schema written to {output}[/green]")
        else:
            # Print to stdout
            print(result)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    app()
