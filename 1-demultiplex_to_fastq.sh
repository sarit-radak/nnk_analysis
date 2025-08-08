#!/bin/bash
#SBATCH --job-name=demux
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --exclusive
#SBATCH --time=72:00:00
#SBATCH --output=logs/demux.%J.out
#SBATCH --error=logs/demux.%J.err

exec > logs/count_nnk.log 2>&1

module purge
module load bcl2fastq/2.19.1.403
mkdir -p 1_raw_fastq

#For code set up, make sure all data files are in L001 AND RunInfo.xml is also in L001

# NextSeq data directory; sub-directories Autocenter, autofocus, etc
RUNFOLDER_DIR="250714_VH00464_562_AAH53NTM5"
# Directory where the output files will go
OUTPUT_DIR="1_raw_fastq/"
# Spreadsheet that specifies the sample barcodes
SAMPLE_SHEET="barcodes.csv"

# Run bcl2fastq with proper paths
bcl2fastq --runfolder-dir "$RUNFOLDER_DIR" --output-dir "$OUTPUT_DIR" --sample-sheet "$SAMPLE_SHEET"

# count reads in each library
cd 1_raw_fastq/Project
find . -type f -name "*_R1_001.fastq" | while read -r file; do
    
    # Get the base filename
    filename=$(basename "$file")
    
    # Extract the library name (everything before _R1_001.fastq)
    libname="${filename%_R1_001.fastq}"

    # Count number of sequences (each sequence starts with @ in FASTQ format)
    count=$(grep -c '^@' "$file")

    # Print result
    echo -e "${libname}\t${count}"
done