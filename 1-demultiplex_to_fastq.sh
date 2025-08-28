#!/bin/bash
#SBATCH --job-name=demux
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --exclusive
#SBATCH --time=72:00:00
#SBATCH --output=logs/demux.out
#SBATCH --error=logs/demux.err

#SBATCH --partition=highmem

module purge
module load bcl2fastq/2.19.1.403

mkdir -p 1_raw_fastq
mkdir -p logs

exec > logs/count_nnk.log 2>&1

#For code set up, make sure all data files are in L001 AND RunInfo.xml is also in L001

# NextSeq data directory; sub-directories Autocenter, autofocus, etc
RUNFOLDER_DIR="250819_VH00124_218_AAHCF7MM5"
# Directory where the output files will go
OUTPUT_DIR="1_raw_fastq/"
# Spreadsheet that specifies the sample barcodes
SAMPLE_SHEET="barcodes.csv"

# run bcl2fastq with proper paths
#bcl2fastq --runfolder-dir "$RUNFOLDER_DIR" --output-dir "$OUTPUT_DIR" --sample-sheet "$SAMPLE_SHEET"

# unzip fastq files
#for file in $(find . -type f -name "*.fastq.gz"); do
#    echo "Unzipping $file..."
#    gunzip "$file"
#done

# count reads in each library
#cd 1_raw_fastq/project
#find . -type f -name "*_R1_001.fastq" | while read -r file; do
    # Get the base filename
#    filename=$(basename "$file")
    
    # Extract the library name (everything before _R1_001.fastq)
#    libname="${filename%_R1_001.fastq}"

    # Count number of sequences (each sequence starts with @ in FASTQ format)
#    count=$(grep -c '^@' "$file")

    # Print result
#    echo -e "${libname}\t${count}"
#done