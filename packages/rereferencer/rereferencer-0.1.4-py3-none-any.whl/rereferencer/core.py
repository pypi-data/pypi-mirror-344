"""Core functionality for primer matching and region extraction."""

from typing import List, Tuple, Optional, Dict
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqUtils import nt_search
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.console import Console
import gffutils
import re

console = Console()

def load_primers(primer_file: str) -> pd.DataFrame:
    """Load primer pairs from CSV file."""
    return pd.read_csv(primer_file)

def parse_gff_gtf(gff_file: str) -> Dict[str, Dict[str, int]]:
    """Parse GFF/GTF file and return a dictionary of gene info."""
    gene_info = {}
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Parsing GFF/GTF file...", total=None)
        
        with open(gff_file, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                
                fields = line.strip().split('\t')
                if len(fields) < 9:
                    continue
                    
                if fields[2] == 'CDS':
                    attributes = fields[8]
                    name_match = re.search(r'Name=([^;]+)', attributes)
                    if name_match:
                        gene_name = name_match.group(1)
                        seqid = fields[0]
                        start = int(fields[3])
                        end = int(fields[4])
                        strand = fields[6]
                        
                        gene_info[gene_name] = {
                            'seqid': seqid,
                            'start': start,
                            'end': end,
                            'strand': strand
                        }
    
    return gene_info

def reverse_complement(seq: str) -> str:
    """Return the reverse complement of a DNA sequence."""
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A',
                 'a': 't', 'c': 'g', 'g': 'c', 't': 'a'}
    return ''.join(complement.get(base, base) for base in reversed(seq))

def remove_tail(primer: str, tail: Optional[str]) -> str:
    """Remove 5' tail from primer sequence if present.
    
    Args:
        primer: The primer sequence
        tail: The 5' tail sequence to remove (in 5'-3' direction)
        
    Returns:
        The primer sequence with tail removed if present, otherwise original sequence
    """
    if not tail:
        return primer
        
    # Clean sequences
    primer = primer.replace(" ", "").upper()
    tail = tail.replace(" ", "").upper()
    
    # Check if primer starts with tail (case-insensitive)
    if primer.upper().startswith(tail.upper()):
        console.print(f"[yellow]Removing 5' tail {tail} from primer {primer}[/]")
        return primer[len(tail):]
    return primer

def find_primer_matches(seq: str, primer: str) -> List[int]:
    """Find all exact matches of a primer in a sequence using BioPython's nt_search.
    
    Args:
        seq: The sequence to search in
        primer: The primer sequence to search for
    """
    matches = []
    
    # Clean sequences by removing spaces and converting to uppercase
    seq = seq.replace(" ", "").upper()
    primer = primer.replace(" ", "").upper()
    
    # Debug logging
    console.print(f"[blue]Debug: Searching for primer: {primer}[/]")
    console.print(f"[blue]Debug: In sequence: {seq[:100]}...[/]")
    
    # Use string find for exact matches only, avoiding overlaps
    pos = 0
    while True:
        pos = seq.find(primer, pos)
        if pos == -1:
            break
        matches.append(pos)
        console.print(f"[green]Debug: Found match at position {pos}[/]")
        pos += len(primer)  # Skip past the entire primer to avoid overlaps
    
    if matches:
        console.print(f"[green]Found {len(matches)} exact matches[/]")
    else:
        console.print(f"[yellow]No matches found for primer: {primer}[/]")
    
    return matches

def extract_region(
    seq: str,
    forward_primer: str,
    reverse_primer: str,
    remove_primers: bool = False,
    forward_tail: Optional[str] = None,
    reverse_tail: Optional[str] = None
) -> Optional[Tuple[int, int, bool, str]]:
    """Extract region between primer pairs using BioPython's sequence matching.
    
    Returns:
        Tuple of (start, end, needs_rc, primer_name) or None if no match
    """
    seq_obj = Seq(seq)
    
    # Debug logging
    console.print(f"[blue]Debug: Processing primer pair:[/]")
    console.print(f"[blue]Debug: Forward: {forward_primer}[/]")
    console.print(f"[blue]Debug: Reverse: {reverse_primer}[/]")
    
    # Remove tails if specified
    original_forward = forward_primer
    original_reverse = reverse_primer
    forward_primer = remove_tail(forward_primer, forward_tail)
    reverse_primer = remove_tail(reverse_primer, reverse_tail)
    
    if forward_tail or reverse_tail:
        console.print(f"[blue]Debug: After tail removal:[/]")
        console.print(f"[blue]Debug: Forward: {forward_primer}[/]")
        console.print(f"[blue]Debug: Reverse: {reverse_primer}[/]")
    
    forward_obj = Seq(forward_primer)
    reverse_obj = Seq(reverse_primer)
    
    # Try both orientations
    orientations = [
        (str(seq_obj), str(seq_obj.reverse_complement()), False),  # Forward orientation
        (str(seq_obj.reverse_complement()), str(seq_obj), True)    # Reverse orientation
    ]
    
    for seq_forward, seq_reverse, needs_rc in orientations:
        forward_matches = find_primer_matches(seq_forward, str(forward_obj))
        reverse_matches = find_primer_matches(seq_reverse, str(reverse_obj))
        
        if forward_matches and reverse_matches:
            # Find the first valid pair where reverse comes after forward
            for f_pos in forward_matches:
                for r_pos in reverse_matches:
                    # Convert reverse position to original sequence coordinates if needed
                    r_pos_orig = len(seq) - r_pos - len(reverse_primer) if needs_rc else r_pos
                    
                    # Check if positions are valid (either forward before reverse or reverse before forward)
                    if (r_pos_orig > f_pos) or (f_pos > r_pos_orig):
                        start = min(f_pos, r_pos_orig)
                        end = max(f_pos + len(forward_primer), r_pos_orig + len(reverse_primer))
                        
                        if remove_primers:
                            if f_pos < r_pos_orig:
                                start += len(forward_primer)
                                end -= len(reverse_primer)
                            else:
                                start += len(reverse_primer)
                                end -= len(forward_primer)
                        
                        console.print(f"[green]Debug: Found valid region at {start}-{end}[/]")
                        return (start, end, needs_rc, original_forward)
    
    console.print("[red]Debug: No valid primer pair positions found[/]")
    return None

def rereference_sequence(seq: str, ref_pos: int, window_size: int = 1000) -> str:
    """Re-reference sequence to a specific position with a window size."""
    seq_len = len(seq)
    half_window = window_size // 2
    
    # Calculate start and end positions relative to ref_pos
    start = max(0, ref_pos - half_window)
    end = min(seq_len, ref_pos + half_window)
    
    # Extract the window
    window = seq[start:end]
    
    # Add N's if needed to maintain window size
    if start == 0:
        window = 'N' * (ref_pos - start) + window
    if end == seq_len:
        window = window + 'N' * (window_size - len(window))
    
    return window

def process_reference(
    reference_file: str,
    primers_df: pd.DataFrame,
    output_file: str,
    remove_primers: bool = False,
    forward_tail: Optional[str] = None,
    reverse_tail: Optional[str] = None,
    gff_file: Optional[str] = None,
    ref_gene: Optional[str] = None,
    window_size: int = 1000
) -> List[SeqRecord]:
    """Process reference sequences and extract amplified regions."""
    results = []
    
    # Track matches by their exact sequence and position
    found_matches = {}  # (seq, start, end) -> primer_name
    
    # Load gene annotations if GFF/GTF file is provided
    gene_info = {}
    ref_pos = None
    if gff_file:
        gene_info = parse_gff_gtf(gff_file)
        if ref_gene:
            if ref_gene in gene_info:
                ref_pos = gene_info[ref_gene]['start']
                console.print(f"[bold green]Found reference gene '{ref_gene}' at position {ref_pos}[/]")
            else:
                console.print(f"[bold red]Warning: Reference gene '{ref_gene}' not found in GFF/GTF file[/]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Processing reference sequences...", total=len(list(SeqIO.parse(reference_file, "fasta"))))
        
        for record in SeqIO.parse(reference_file, "fasta"):
            seq = str(record.seq)
            primer_results = []
            
            for _, row in primers_df.iterrows():
                region = extract_region(
                    seq,
                    row["forward"],
                    row["reverse"],
                    remove_primers,
                    forward_tail,
                    reverse_tail
                )
                
                if region:
                    start, end, needs_rc, matched_primer = region
                    amplified_seq = seq[start:end]
                    
                    # Reverse complement if necessary
                    if needs_rc:
                        amplified_seq = reverse_complement(amplified_seq)
                    
                    # Create a unique key for this match
                    match_key = (amplified_seq, start, end)
                    
                    # If we've seen this exact sequence before, show a warning
                    if match_key in found_matches:
                        console.print(f"[yellow]Warning: Found duplicate match at position {start}-{end} for primer {row['name']} (previously found by {found_matches[match_key]})[/]")
                        continue
                        
                    found_matches[match_key] = row['name']
                    
                    # Get gene name if available
                    gene_name = ""
                    for name, info in gene_info.items():
                        if info['seqid'] == record.id and start >= info['start'] and end <= info['end']:
                            gene_name = name
                            break
                    
                    # Re-reference if requested
                    if ref_pos is not None:
                        # Calculate relative position in the amplified sequence
                        rel_pos = ref_pos - start if not needs_rc else end - ref_pos
                        amplified_seq = rereference_sequence(amplified_seq, rel_pos, window_size)
                    
                    gene_suffix = f"_{gene_name}" if gene_name else ""
                    amplicon_size = len(amplified_seq)
                    new_record = SeqRecord(
                        Seq(amplified_seq),
                        id=f"{record.id}_{row['name']}{gene_suffix}_size{amplicon_size}",
                        description=f"Amplified_region_from_{record.id}_using_{row['name']}_at_{start}-{end}"
                    )
                    primer_results.append(new_record)
            
            results.extend(primer_results)
            progress.update(task, advance=1)
    
    # Create summary table
    table = Table(title="Primer Matching Summary")
    table.add_column("Primer Pair")
    table.add_column("Matches Found")
    
    for name in primers_df["name"]:
        matches = sum(1 for r in results if name in r.id)
        table.add_row(name, str(matches))
    
    console.print(table)
    
    # Write results to file with single-line sequences
    if results:
        with open(output_file, 'w') as f:
            for record in results:
                f.write(f">{record.id}\n")
                f.write(f"{str(record.seq)}\n")
    
    return results 