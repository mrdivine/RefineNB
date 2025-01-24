"""Command line interface for RefineNB."""

import sys
from pathlib import Path

import click
from rich.console import Console

from src.output import extract_notebook_to_json
from src.translate import NotebookTranslator
from src.utils import NotebookValidationError

console = Console()

@click.group()
def main():
    """RefineNB - Translate and extract content from Jupyter notebooks."""
    pass

@main.command()
@click.option(
    "--notebook-path",
    "-nb",
    required=True,
    type=click.Path(exists=True),
    help="Path to the input notebook",
)
@click.option(
    "--language",
    "-l",
    required=True,
    type=str,
    help="Target language code (e.g., 'DE' for German)",
)
def translate(notebook_path: str, language: str):
    """Translate notebook content to the specified language."""
    console.print(f"[bold green]Translating notebook:[/] {notebook_path}")
    console.print(f"[bold green]Target language:[/] {language}")
    # TODO: Implement translation logic
    raise NotImplementedError("Translation functionality not yet implemented")

@main.command()
@click.option(
    "--notebook-path",
    "-nb",
    required=True,
    type=click.Path(exists=True),
    help="Path to the input notebook",
)
@click.option(
    "--output",
    "-o",
    required=True,
    type=click.Path(),
    help="Path to save the output JSON file",
)
def output(notebook_path: str, output: str):
    """Extract notebook content to JSON format."""
    try:
        console.print(f"[bold green]Extracting from notebook:[/] {notebook_path}")
        console.print(f"[bold green]Output path:[/] {output}")
        extract_notebook_to_json(notebook_path, output)
        console.print(f"[bold green]Successfully extracted content to:[/] {output}")
        return 0
    except NotebookValidationError as e:
        console.print(f"[bold red]Error:[/] Invalid notebook structure - {str(e)}")
        return 1
    except ValueError as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        return 1
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/] {str(e)}")
        return 1

if __name__ == "__main__":
    main() 