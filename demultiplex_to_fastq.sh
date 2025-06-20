#!/bin/bash
#SBATCH --job-name=demux
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=72:00:00
#SBATCH --output=logs/demux.%J.out
#SBATCH --error=logs/demux.%J.err

cd $SUBMIT_SLURM_DIR
module purge
module load bcl2fastq/2.19.1.403
cd Documents/NextSeq

#For code set up, make sure all data files are in L001 AND RunInfo.xml is also in L001

# Define paths for bcl2fastq

# NextSeq data directory; sub-directories Autocenter, autofocus, etc
RUNFOLDER_DIR="/gpfs/home/sradak/25-06-02_Interface_L4/250530_VH00124_207_AAH2J32M5"
# Directory where the output files will go
OUTPUT_DIR="/gpfs/home/sradak/25-06-02_Interface_L4/raw_fastq"
# Spreadsheet that specifies the sample barcodes
SAMPLE_SHEET="/gpfs/home/sradak/25-06-02_Interface_L4/barcodes.csv"

# Run bcl2fastq with proper paths
bcl2fastq --runfolder-dir "$RUNFOLDER_DIR" --output-dir "$OUTPUT_DIR" --sample-sheet "$SAMPLE_SHEET"