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

def find_primer_matches(seq: str, primer: str, strict_5prime: bool = False) -> List[int]:
    """Find all matches of a primer in a sequence using BioPython's nt_search."""
    matches = []
    
    # Clean sequences by removing spaces and converting to uppercase
    seq = seq.replace(" ", "").upper()
    primer = primer.replace(" ", "").upper()
    
    # Find all matches using BioPython's nt_search
    all_matches = nt_search(seq, primer)
    if len(all_matches) > 1:  # First element is the pattern, rest are positions
        matches = all_matches[1:]
    
    if strict_5prime:
        # Filter for matches that start with the first 10 bases
        primer_start = primer[:10]
        matches = [pos for pos in matches if seq[pos:pos+10] == primer_start]
    
    return matches

def extract_region(
    seq: str,
    forward_primer: str,
    reverse_primer: str,
    remove_primers: bool = False,
    strict_5prime: bool = False
) -> Optional[Tuple[int, int, bool]]:
    """Extract region between primer pairs using BioPython's sequence matching."""
    # Try forward orientation first
    forward_matches = find_primer_matches(seq, forward_primer, strict_5prime)
    reverse_matches = find_primer_matches(seq, reverse_primer, strict_5prime)
    
    # If no matches in forward orientation, try reverse orientation
    if not forward_matches or not reverse_matches:
        forward_matches = find_primer_matches(seq, reverse_primer, strict_5prime)
        reverse_matches = find_primer_matches(seq, forward_primer, strict_5prime)
        if forward_matches and reverse_matches:
            # Swap primers since we're in reverse orientation
            forward_matches, reverse_matches = reverse_matches, forward_matches
    
    if not forward_matches or not reverse_matches:
        return None
    
    # Find the first valid pair where reverse comes after forward
    for f_pos in forward_matches:
        for r_pos in reverse_matches:
            if r_pos > f_pos:
                start = f_pos
                end = r_pos + len(reverse_primer)
                if remove_primers:
                    start += len(forward_primer)
                    end -= len(reverse_primer)
                return (start, end, False)
    
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
    strict_5prime: bool = False,
    gff_file: Optional[str] = None,
    ref_gene: Optional[str] = None,
    window_size: int = 1000
) -> List[SeqRecord]:
    """Process reference sequences and extract amplified regions."""
    results = []
    
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
                    strict_5prime
                )
                
                if region:
                    start, end, needs_rc = region
                    amplified_seq = seq[start:end]
                    
                    # Reverse complement if necessary
                    if needs_rc:
                        amplified_seq = reverse_complement(amplified_seq)
                    
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
                        description=f"Amplified_region_from_{record.id}_using_{row['name']}"
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