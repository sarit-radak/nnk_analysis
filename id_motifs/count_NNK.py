from collections import defaultdict
from Bio.Seq import Seq
from Bio import SeqIO
import pandas as pd
import re
import sys
import os

IUPAC_DICT = {
    'A': 'A', 'T': 'T', 'C': 'C', 'G': 'G',
    'R': '[AG]', 'Y': '[CT]', 'S': '[GC]', 'W': '[AT]',
    'K': '[GT]', 'M': '[AC]', 'B': '[CGT]', 'D': '[AGT]',
    'H': '[ACT]', 'V': '[ACG]', 'N': '[ATCG]'
}

def degenerate_to_regex(seq):
    return ''.join(IUPAC_DICT.get(base, base) for base in seq.upper())

def load_motifs(motif_file):
    """Load motifs from the Excel file, replacing NNK with a regex pattern."""
    df = pd.read_excel(motif_file)
    motifs = df[["Sequence Name", "NNK Context"]].dropna()
    motif_patterns = {
    row["Sequence Name"]: degenerate_to_regex(row["NNK Context"])
    for _, row in motifs.iterrows()
}
    return motif_patterns

def bracket_to_iupac(seq):
    """Convert bracketed degenerate bases to IUPAC shorthand."""
    iupac_map = {
        frozenset("A"): "A",
        frozenset("C"): "C",
        frozenset("G"): "G",
        frozenset("T"): "T",
        frozenset("AG"): "R",
        frozenset("CT"): "Y",
        frozenset("CG"): "S",
        frozenset("AT"): "W",
        frozenset("GT"): "k",
        frozenset("AC"): "M",
        frozenset("CGT"): "B",
        frozenset("AGT"): "D",
        frozenset("ACT"): "H",
        frozenset("ACG"): "V",
        frozenset("ACGT"): "n",
    }

    import re

    output = ""
    i = 0
    while i < len(seq):
        if seq[i] == "[":
            j = seq.find("]", i)
            if j == -1:
                raise ValueError("Unmatched [ in sequence")
            bases = seq[i+1:j]
            key = frozenset(bases.upper())
            if key not in iupac_map:
                raise ValueError(f"Unknown degenerate base: [{bases}]")
            output += iupac_map[key]
            i = j + 1
        else:
            output += seq[i]
            i += 1
    return output

def count_motifs_in_fasta(fasta_file, motifs, out_prefix):
    """Iterate through FASTA, find motifs, and count amino acids translated from the middle codon."""

    motif_aa_counts = defaultdict(lambda: defaultdict(int))
    zero_motif_seqs = []
    one_motif_seqs = []
    multi_motif_seqs = []

    for record in SeqIO.parse(fasta_file, "fasta"):
        seq = str(record.seq).upper()
        
        matched_motifs = []
        motif_matches = {}

        # First: find which motifs match
        for motif, pattern in motifs.items():
            match = re.search(pattern, seq)
            if match:
                matched_motifs.append([motif, pattern])
                motif_matches[motif] = match
        
        # Proceed only if exactly one motif matches
        if len(matched_motifs) == 0:
            zero_motif_seqs.append(record)
        elif len(matched_motifs) == 1:
            one_motif_seqs.append(record)
        else:
            multi_motif_seqs.append(record)
        
        if len(matched_motifs) == 1:
            motif = matched_motifs[0][0]
            pattern = matched_motifs[0][1]
            match = motif_matches[motif]
            matched_seq = match.group()

            nnk_index = (len(str(pattern).split("[")[0]))
            

            middle_codon = matched_seq[nnk_index:nnk_index+3]
            aa = str(Seq(middle_codon).translate())
            motif_aa_counts[motif][aa] += 1
    
    SeqIO.write(zero_motif_seqs, f"{out_prefix}_0_nnk.fasta", "fasta")
    SeqIO.write(one_motif_seqs, f"{out_prefix}_1_nnk.fasta", "fasta")
    SeqIO.write(multi_motif_seqs, f"{out_prefix}_multi_nnk.fasta", "fasta")

    return motif_aa_counts

def save_counts_to_excel(motif_aa_counts, motif_patterns, output_file):
    """Save motif amino acid counts to an Excel file."""
    standard_aas = ["A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", 
                    "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V", "*"]
    all_aas = standard_aas


    rows = []
    for motif, aa_counts in motif_aa_counts.items():
        row = {"Motif": motif, "Sequence": bracket_to_iupac(motif_patterns[motif])}
        total = 0
        aa_counts = motif_aa_counts.get(motif, {})  # Default to empty if motif is not found

        for aa in all_aas:
            count = aa_counts.get(aa, 0)
            row[aa] = count
            total += count
        row["Total"] = total
        rows.append(row)
        # Add rows for motifs not found

    for motif in motif_patterns.keys():
        if motif not in motif_aa_counts:
            row = {"Motif": motif, "Sequence": bracket_to_iupac(motif_patterns[motif])}
            for aa in all_aas:
                row[aa] = 0
            row["Total"] = 0
            rows.append(row)

    # Ensure all amino acids are represented as columns with zeroes if not found
    for row in rows:
        for aa in all_aas:
            if aa not in row:
                row[aa] = 0

    df = pd.DataFrame(rows)
    df.to_excel(output_file, index=False)


if not((len(sys.argv) !=2) or (len(sys.argv) !=3)):
    print("Usage: python3 -u count_nnk.py motif_file (optional)")
    sys.exit(1)


fasta_file = sys.argv[1]

if len(sys.argv) == 2: # motif file not specified
    if "A3" in fasta_file:
        motif_file = "id_motifs/A3_motifs.xlsx"
    elif "B2M" in fasta_file:
        motif_file = "id_motifs/B2M_motifs.xlsx"
    elif "A4" in fasta_file:
        motif_file = "id_motifs/A4_motifs.xlsx"
    else:
        print(f"Unknown library type in {fasta_file}. Please specify a motif file.")
        sys.exit(1)

    output_excel_path = fasta_file.replace("hypermut_filtered/", "nnk_count/")
    output_excel_path = output_excel_path.replace(".fasta", ".xlsx")
    output_excel_path = output_excel_path.replace("_hypermut", "")


else: # motif file specified
    motif_file = sys.argv[2]
    output_excel_path = fasta_file.replace("hypermut_filtered/", "nnk_count/")
    output_excel_path = output_excel_path.replace(".fasta", f"_vs_{motif_file.replace("xlsx","").replace("id_motifs/","")}.xlsx")


motifs = load_motifs(motif_file)
output_prefix = fasta_file.replace("hypermut_filtered/", "nnk_count/fasta_stratified_by_count/").replace(".fasta", "")
motif_counts = count_motifs_in_fasta(fasta_file, motifs, output_prefix)
save_counts_to_excel(motif_counts, motifs, output_excel_path)

print("Motif counting complete. Results saved to:", output_excel_path)