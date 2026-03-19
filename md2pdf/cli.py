"""Command-line interface for md2pdf."""

import subprocess
import sys
from pathlib import Path

import click

from .converter import convert


@click.command()
@click.version_option("0.2.0", "-v", "--version")
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "-o", "--output",
    type=click.Path(path_type=Path),
    help="Output PDF path. Defaults to input filename with .pdf extension.",
)
@click.option(
    "--css",
    type=click.Path(exists=True, path_type=Path),
    help="Custom CSS stylesheet to override default styles.",
)
@click.option(
    "--open",
    "open_after",
    is_flag=True,
    help="Open the PDF after conversion.",
)
def main(input_file: Path, output: Path | None, css: Path | None, open_after: bool):
    """Convert Markdown to professional PDF.
    
    Takes a Markdown file and converts it to a polished PDF document.
    Supports custom syntax extensions for page breaks (---break---),
    centering (-> text <-), and page numbers via frontmatter.
    
    Examples:
    
        md2pdf document.md
        
        md2pdf document.md -o report.pdf
        
        md2pdf document.md --css custom.css --open
    """
    try:
        output_path = convert(input_file, output, css)
        click.echo(f"✓ Created {output_path}")
        
        if open_after:
            _open_file(output_path)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def _open_file(path: Path) -> None:
    """Open a file with the system default application."""
    if sys.platform == "darwin":
        subprocess.run(["open", str(path)])
    elif sys.platform == "win32":
        subprocess.run(["start", str(path)], shell=True)
    else:
        # Linux and other Unix-like systems
        subprocess.run(["xdg-open", str(path)])


if __name__ == "__main__":
    main()
