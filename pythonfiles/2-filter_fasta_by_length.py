import sys
import os
from Bio import SeqIO

def filter_fasta(input_file, length_cutoff, output_dir):
    basename = os.path.basename(input_file)
    output_path = os.path.join(output_dir, basename)

    with open(input_file, "r") as infile, open(output_path, "w") as outfile:
        records = (record for record in SeqIO.parse(infile, "fasta") if len(record.seq) >= length_cutoff)
        count = SeqIO.write(records, outfile, "fasta")

    print(f"Wrote {count} sequences to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input_fasta> <length_cutoff>")
        sys.exit(1)

    input_fasta = sys.argv[1]
    cutoff = int(sys.argv[2])
    
    filter_fasta(input_fasta, cutoff, "3_len_filtered/")