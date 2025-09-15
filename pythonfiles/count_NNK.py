from collections import defaultdict

from numpy import lib
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
    motifs = df[["Oligo", "NNK Motif"]].dropna()
    motif_patterns = {
    row["Oligo"]: degenerate_to_regex(row["NNK Motif"])
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

def get_matches (seq):
    seq_rc = str(Seq(seq).reverse_complement())


    # find motifs in read
    matched_motifs = []
    motif_matches = {}
    for motif, pattern in motifs.items():
        match = re.search(pattern, seq)
        if match:
            matched_motifs.append([motif, pattern])
            motif_matches[motif] = match
    
    # find motifs in reverse complement of read
    matched_motifs_rc = []
    motif_matches_rc = {}
    for motif, pattern in motifs.items():
        match = re.search(pattern, seq_rc)
        if match:
            matched_motifs_rc.append([motif, pattern])
            motif_matches_rc[motif] = match
    
    print (len(matched_motifs), len(matched_motifs_rc))

    if (len(matched_motifs) == 1) & (len(matched_motifs_rc) != 1): # one match in read, not one match in reverse complement
        return matched_motifs, motif_matches
    
    elif (len(matched_motifs) != 1) & (len(matched_motifs_rc) == 1): # not one match in read, one match in reverse complement
        return matched_motifs_rc, motif_matches_rc
    
    elif (len(matched_motifs) == 0) & (len(matched_motifs_rc) == 0): # no motifs in forward or reverse complement
        return matched_motifs, motif_matches

    else:
        return [0,0,0], [0,0,0] # lists long enough to handle the sequence as containing multiple motifs

def count_motifs_in_fasta(library, motifs, out_prefix):
    """Iterate through FASTA, find motifs, and count amino acids translated from the middle codon."""
    
    fasta_file = f"libraries/{library}/{library}_len_pass.fasta"

    motif_aa_counts = defaultdict(lambda: defaultdict(int))
    zero_motif_seqs = []
    one_motif_seqs = []
    multi_motif_seqs = []

    for record in SeqIO.parse(fasta_file, "fasta"):
        seq = str(record.seq).upper()
        
        matched_motifs, motif_matches = get_matches (seq)
        
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
        parts = motif.split('_')
        label = parts[1] + " " + parts[3] # protein + wt residue + residue number
        row = {"Position": label}
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
            parts = motif.split('_')
            label = parts[1] + " " + parts[3] # protein + wt residue + residue number
            row = {"Position": label}
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

    # sort by amino acid number
    df["__sort_key__"] = df["Position"].astype(str).str.extract(r'(\d+)$').astype(int)
    df = df.sort_values("__sort_key__")
    df = df.drop(columns="__sort_key__")            

    # sort mu alphabetically
    columns = df.columns.tolist()
    position = ["Position"]
    stop = ['*']
    total = ['Total']
    aa_columns = sorted([col for col in columns if col not in position + stop + total])
    new_column_order = position + stop + aa_columns + total
    df = df[new_column_order]
    
    df_t = df.set_index("Position").T


    df_t.to_excel(output_file, index=True)


library = sys.argv[1]


if "A3" in library:
    motif_file = "L4_A3_motifs.xlsx"
elif "B2M" in library:
    motif_file = "L4_B2M_motifs.xlsx"
else:
    print ("name ambiguous, using B2M motifs")
    motif_file = "L4_B2M_motifs.xlsx"


motifs = load_motifs(motif_file)

# specify the name of the count file
output_excel_path = f"libraries/{library}/{library}.xlsx"

# specify where the fasta files will be saved
output_prefix = f"libraries/{library}/{library}"
motif_counts = count_motifs_in_fasta(library, motifs, output_prefix)
save_counts_to_excel(motif_counts, motifs, output_excel_path)

print(f'{library} nnk counted')