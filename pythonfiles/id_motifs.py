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
'''
def degenerate_to_regex(seq):
    return ''.join(IUPAC_DICT.get(base, base) for base in seq.upper())

def count_degenerate_matches(degenerate_seq, reference_seq):
    pattern = degenerate_to_regex(degenerate_seq)
    matches = re.findall(f'(?={pattern})', reference_seq.upper())
    return len(matches)

def find_nnk_and_context(reference, sequence, oPool_frame): # this function dynamically adjusts boundaries such that it returns two codons before and two codons after the synonomous mutations; I've changed things so it alwayhs returns three codons on either side
    """
    Aligns the sequence with the reference, identifies the first and last mismatch,
    and expands the boundaries to ensure a full codon frame (multiples of 3).
    """

    mismatches = [i for i in range(len(reference)) if reference[i] != sequence[i]]

    if not mismatches:
        return None  # No differences found (unexpected case)
    
    first_mismatch = mismatches[0]
    last_mismatch = mismatches[-1]
    
    # Adjust to ensure the region is in frame
    offset = oPool_frame-1
    start_pos = first_mismatch - ((first_mismatch-offset) % 3)-3  # Move back to start of codon, include one extra codons
    end_pos = last_mismatch + (3 - ((last_mismatch-offset) % 3))+3  # Move forward to end of codon, include one extra codons
    
    motif = sequence[start_pos:end_pos] 
    
    return motif
    
'''
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

def process_fasta(fasta_file, output_file):
    for record in SeqIO.parse(fasta_file, "fasta"):
        
        if "A3" in record.id:
            reference_seq = A3
            frame = oPool_frame = 3
        elif "B2M_oPool1" in record.id:
            reference_seq = B2M_1
            frame = oPool_frame = 1
        elif "B2M_oPool2" in record.id:
            reference_seq = B2M_2
            frame = oPool_frame = 3


        reference = str(reference_seq).upper()    
        sequence = str(record.seq).upper()
        
        context = extract_context(sequence)
        
        data.append([record.id, context])

    df = pd.DataFrame(data, columns=["Sequence Name", "NNK Context"])
    df.to_excel(output_file, index=False)


# Example usage
oPool_frame = 3

data = []


A3 = "GTAGACCTGAGGATAAAGTTACATTAACTTGTCATGTTCTCGGTTTCTATCCGGCAGACATTACTCTTACATGGCAACTTAATGGTGAAGAGTTGATTCAGGACATGGAGCTCACAGAGACGGTTCCTGCTGGAGACGGCACCTATCAGAAGTGGGCGTCCGTTGTTGTTCCACTTGGAAAAGAACAGTATTATACATGTCATGTTTATCATCAAGGATTACCAGAGCCTTTAACATTACGTTGGGAGCCGCCACCATCCACAGGAGGATCCGGAGGCGAACA"
B2M_1 = "ATGTCCGCTGTTTTGTTGTTGGCCTTGCTAGGTTTCATTCTGCCATTACCAGGTGTGCAAGCCTCTATCATTAACTTCGAGAAGTTGGGTGGAGGTGCATCAGGAGGAGGTAACCCAAACGCTAATCCAAACGCTAATCCTAATGCTGGCTGGGAATTGCAAGATTACAAGGAAAAGGAAACTACCGGTATTCAAAAAACACCACAAGTTTACGTCTACTCGAGACATCCACCTGAAAATGGAAAACCAAACATTTTGAACTGCTATGTTACTCAATTCCACCCACCTCATATTGAAATTCAGATGCTTAAGAATGGTAAAAAGATTCCAAAAGTTGAAATGTCAGAC"
B2M_2 = "TGCAAGATTACAAGGAAAAGGAAACTACCGGTATTCAAAAAACACCACAAGTTTACGTCTACTCGAGACATCCACCTGAAAATGGAAAACCAAACATTTTGAACTGCTATGTTACTCAATTCCACCCACCTCATATTGAAATTCAGATGCTTAAGAATGGTAAAAAGATTCCAAAAGTTGAAATGTCAGACATGAGTTTCTCAAAGGATTGGTCATTCTATATTCTTGTTCATACAGAGTTCACACCAACAGAAACAGATACATACGCTTGTAGAGTCAAACATGCATCGATGGCTGAACCTAAAACAGTTTACTGGGATAGAGATATGGGATCTGGTGACAAGACTCAC"


fasta_file = sys.argv[1]

fasta_file_path = f"id_motifs/{fasta_file}"

output_excel_path = fasta_file_path.replace("_oPool_NNK.fasta", "_motifs.xlsx")

process_fasta(fasta_file_path, output_excel_path)