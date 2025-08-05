#!/bin/bash
#SBATCH --job-name=count_nnk
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --exclusive
#SBATCH --time=72:00:00
#SBATCH --output=logs/count_nnk.out
#SBATCH --error=logs/count_nnk.err

exec > logs/count_nnk.log 2>&1

# Function to count NNKs
run_count() {
    fasta="$1"
    motifs="L6_FLAG_motifs.xlsx"
    python3 -u pythonfiles/3-count_NNK.py "$motifs" "$fasta"
}
export -f run_count

# count NNKs in test set
#python3 -u pythonfiles/4-count_NNK.py 4_id_motifs/A3_oPool_NNK_motifs.xlsx 3_len_filtered/nnk_motif_test_set.fasta

# count NNKs in all reads
#find 3_len_filtered -type f -name '*.fasta' | parallel -j 16 run_count

# count the number of sequences with 0, 1, and multiple motifs
#python3 -u pythonfiles/4-count_NNK_per_read.py