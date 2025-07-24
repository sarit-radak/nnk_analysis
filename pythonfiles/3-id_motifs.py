from Bio import SeqIO
import pandas as pd
import re
import sys

# IUPAC codes as regex patterns
IUPAC_DICT = {
    'A': 'A',
    'T': 'T',
    'C': 'C',
    'G': 'G',
    'R': '[AG]',
    'Y': '[CT]',
    'S': '[GC]',
    'W': '[AT]',
    'K': '[GT]',
    'M': '[AC]',
    'B': '[CGT]',
    'D': '[AGT]',
    'H': '[ACT]',
    'V': '[ACG]',
    'N': '[ATCG]'
}

def extract_context(seq, motif="NNK", codons_before=3, codons_after=3):
    # Find index of motif
    idx = seq.find(motif)
    if idx == -1:
        raise ValueError(f"Motif '{motif}' not found in sequence.")
    
    # Calculate span
    start = idx - codons_before * 3
    end = idx + len(motif) + codons_after * 3

    # Check bounds
    if start < 0 or end > len(seq):
        raise ValueError("Not enough context before or after motif.")

    context_seq = seq[start:end]
    return context_seq

def process_fasta(fasta_file, output_file, reference):
    for record in SeqIO.parse(fasta_file, "fasta"):
        
        reference = str(reference).upper()    
        sequence = str(record.seq).upper()
        
        context = extract_context(sequence)
        
        data.append([record.id, context])

    df = pd.DataFrame(data, columns=["Sequence Name", "NNK Context"])
    df.to_excel(output_file, index=False)





fasta_file = sys.argv[1]
reference = sys.argv[2]
fasta_file_path = f"4_id_motifs/{fasta_file}"
output_excel_path = fasta_file_path.replace(".fasta", "_motifs.xlsx")


data = []
process_fasta(fasta_file_path, output_excel_path, reference)