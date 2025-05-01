# Primer Extractor

A tool for extracting amplified regions from reference sequences using primer pairs.

## Installation

```bash
pip install rereferencer
```

## Usage

The tool can be used to extract amplified regions from reference sequences using primer pairs. It supports:
- FASTA reference sequences
- GFF/GTF annotation files
- Primer pairs in CSV format
- Progress bars for long-running operations
- Rich table output for results

### Command Line Interface

```bash
Usage: rereferencer [OPTIONS]

Options:
  --primer-file PATH     CSV file containing primer pairs (name, forward, reverse) [required]
  --reference PATH       Reference sequence file in FASTA format [required]
  --output PATH          Output file for amplified regions in FASTA format [required]
  --remove-primers       Remove primer sequences from the output
  --forward-tail TEXT    5' tail sequence (5'-3' direction) to remove from forward primers
  --reverse-tail TEXT    5' tail sequence (5'-3' direction) to remove from reverse primers
  --gff PATH            GFF/GTF file for gene annotations
  --ref-gene TEXT       Reference gene name for re-referencing sequences
  --window-size INTEGER Window size for re-referencing (default: 1000)
  --help                Show this message and exit.
```

### Examples

```bash
# Basic usage with progress bar
rereferencer \
    --primer-file example_primers.csv \
    --reference references/Mycobacterium_tuberculosis_H37Rv_genome_v4.fasta \
    --output mtb_amplicons.fasta

# Using GFF annotations and re-referencing to a specific gene
rereferencer \
    --primer-file example_primers.csv \
    --reference references/Mycobacterium_tuberculosis_H37Rv_genome_v4.fasta \
    --gff references/Mycobacterium_tuberculosis_H37Rv_gff_v4.gff \
    --ref-gene rpoB \
    --window-size 1000 \
    --output mtb_amplicons_rpoB.fasta

# Remove primer sequences and tails from output
rereferencer \
    --primer-file example_primers.csv \
    --reference references/Mycobacterium_tuberculosis_H37Rv_genome_v4.fasta \
    --remove-primers \
    --forward-tail ACGTACGT \
    --reverse-tail TGCATGCA \
    --output mtb_amplicons_no_primers.fasta
```

### Input Files

1. **Primer File (CSV)**
   - Must contain columns: `name`, `forward`, `reverse`
   - Example:
   ```csv
   name,forward,reverse
   rpoB_RRDR,GGGAGCGGATGACCACCC,GCGGTACGGCGTTTCGATGAAC
   katG_315,GCTGATCCACCGCGGCATC,GCCGAGTCGTTCATCGTGCT
   ```

2. **Reference Sequence (FASTA)**
   - Standard FASTA format
   - Can be single or multi-sequence
   - Supports compressed files (.gz, .bz2)

3. **GFF/GTF File (Optional)**
   - Standard GFF/GTF format
   - Used for gene annotations and re-referencing
   - Supports compressed files (.gz, .bz2)

### Output

The tool generates:
1. A FASTA file containing the extracted regions
2. A progress bar showing the processing status
3. A summary table showing the number of matches found for each primer pair
4. Detailed logging of the extraction process

## Features

- **Progress Tracking**: Shows progress bars for long-running operations
- **Rich Output**: Uses rich tables for clear result presentation
- **Flexible Matching**: Supports strict 5' end matching
- **Gene Annotation**: Integrates with GFF/GTF files for gene context
- **Re-referencing**: Can re-reference sequences to specific genes
- **Primer Removal**: Option to remove primer sequences from output
- **Compressed File Support**: Handles gzipped and bzipped input files
- **Detailed Logging**: Comprehensive logging of the extraction process

## Requirements

- Python 3.8+
- click
- biopython
- pandas
- rich

## Author

- **Name**: SemiQuant
- **Email**: JasonLimberis@ucsf.edu
- **GitHub**: [SemiQuant](https://github.com/SemiQuant)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 