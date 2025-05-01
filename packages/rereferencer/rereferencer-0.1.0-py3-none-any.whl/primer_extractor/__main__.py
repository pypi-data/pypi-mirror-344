"""Main entry point for primer extractor."""

import click
from .cli import main

@click.group()
def cli():
    """Primer Extractor - Extract amplified regions from reference sequences."""
    pass

cli.add_command(main)

if __name__ == "__main__":
    cli() 