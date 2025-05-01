"""Command-line interface for primer extractor."""

import click
from Bio import SeqIO
from rich.console import Console
from rich.table import Table
from .core import load_primers, process_reference
from typing import Optional

console = Console()

@click.command(name="extract")
@click.option(
    "--primer-file",
    required=True,
    type=click.Path(exists=True),
    help="CSV file containing primer pairs (name, forward, reverse)"
)
@click.option(
    "--reference",
    required=True,
    type=click.Path(exists=True),
    help="Reference sequence file in FASTA format"
)
@click.option(
    "--output",
    required=True,
    type=click.Path(),
    help="Output file for amplified regions in FASTA format"
)
@click.option(
    "--remove-primers",
    is_flag=True,
    help="Remove primer sequences from the output"
)
@click.option(
    "--strict-5prime",
    is_flag=True,
    help="Require exact match of first 10 bases for 5' end"
)
@click.option(
    "--gff",
    type=click.Path(exists=True),
    help="GFF/GTF file for gene annotations"
)
@click.option(
    "--ref-gene",
    help="Reference gene name for re-referencing sequences"
)
@click.option(
    "--window-size",
    type=int,
    default=1000,
    help="Window size for re-referencing (default: 1000)"
)
def main(
    primer_file: str,
    reference: str,
    output: str,
    remove_primers: bool,
    strict_5prime: bool,
    gff: Optional[str],
    ref_gene: Optional[str],
    window_size: int
):
    """Extract amplified regions from reference sequences using primer pairs."""
    console.print("Loading primers...")
    primers_df = load_primers(primer_file)
    
    console.print("Processing reference sequences...")
    results = process_reference(
        reference,
        primers_df,
        output,
        remove_primers,
        strict_5prime,
        gff,
        ref_gene,
        window_size
    )
    
    if not results:
        console.print("[bold red]No matches found for any primer pairs[/]")
        return
    
    console.print(f"[bold green]Successfully extracted {len(results)} regions[/]")

if __name__ == "__main__":
    main() 