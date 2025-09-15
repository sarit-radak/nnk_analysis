import os
import sys
import gzip
import shutil
from Bio import SeqIO

print ("")
print("Extracting sequences to fasta...")

sample = sys.argv[1]
dir = f"libraries/{sample}"

output_fasta = f"{dir}/{sample}_all.fasta"


# Collect all .fastq and .fastq.gz files from the directory
all_files = os.listdir(dir)
fastq_gz_files = [f for f in all_files if f.endswith('.fastq.gz')]
fastq_files = [f for f in all_files if f.endswith('.fastq')]

# Unzip .fastq.gz files if they haven't been unzipped yet
for gz_file in fastq_gz_files:
    fastq_path = os.path.join(dir, gz_file)
    unzipped_file = os.path.join(dir, gz_file[:-3])  # Remove '.gz'
    
    if not os.path.exists(unzipped_file):  # Check if already unzipped
        print(f"Unzipping {gz_file}...")
        with gzip.open(fastq_path, 'rb') as gz_in:
            with open(unzipped_file, 'wb') as fastq_out:
                shutil.copyfileobj(gz_in, fastq_out)
        fastq_files.append(gz_file[:-3])  # Add to fastq_files list

sequences_written = 0

# Open output file to write
with open(output_fasta, 'w') as fasta_out:
    for fastq_file in fastq_files:
        fastq_path = os.path.join(dir, fastq_file)
        with open(fastq_path, 'r') as handle:
            for record in SeqIO.parse(handle, 'fastq'):
                # Write header
                fasta_out.write(f">{record.id}\n")
                # Write sequence as a single line
                fasta_out.write(f"{str(record.seq)}\n")
                sequences_written += 1

print(f"Extracted {sequences_written} sequences to {output_fasta}")