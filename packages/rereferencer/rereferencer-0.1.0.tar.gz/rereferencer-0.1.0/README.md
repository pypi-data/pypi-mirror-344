# Rereferencer

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

### Example

```bash
# Basic usage with progress bar
rereferencer extract \
    --primer-file example_primers.csv \
    --reference references/Mycobacterium_tuberculosis_H37Rv_genome_v4.fasta \
    --output mtb_amplicons.fasta

# Using GFF annotations and re-referencing to a specific gene
rereferencer extract \
    --primer-file example_primers.csv \
    --reference references/Mycobacterium_tuberculosis_H37Rv_genome_v4.fasta \
    --gff references/Mycobacterium_tuberculosis_H37Rv_gff_v4.gff \
    --ref-gene rpoB \
    --window-size 500 \
    --output mtb_amplicons_rpoB.fasta

# Remove primer sequences from output
rereferencer extract \
    --primer-file example_primers.csv \
    --reference references/Mycobacterium_tuberculosis_H37Rv_genome_v4.fasta \
    --remove-primers \
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

3. **GFF/GTF File (Optional)**
   - Standard GFF/GTF format
   - Used for gene annotations and re-referencing

### Output

The tool generates:
1. A FASTA file containing the extracted regions
2. A progress bar showing the processing status
3. A summary table showing the number of matches found for each primer pair

## Features

- **Progress Tracking**: Shows progress bars for long-running operations
- **Rich Output**: Uses rich tables for clear result presentation
- **Flexible Matching**: Supports strict 5' end matching
- **Gene Annotation**: Integrates with GFF/GTF files for gene context
- **Re-referencing**: Can re-reference sequences to specific genes
- **Primer Removal**: Option to remove primer sequences from output

## Requirements

- Python 3.8+
- click
- biopython
- pandas
- rich 