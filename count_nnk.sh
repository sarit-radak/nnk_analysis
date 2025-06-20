#!/bin/bash
#SBATCH --job-name=count_nnk
#SBATCH --nodes=1
#SBATCH --partition=gpu
#SBATCH --ntasks=16
#SBATCH --time=24:00:00
#SBATCH --output=logs/count_nnk.out
#SBATCH --error=logs/count_nnk.err

exec > logs/count_nnk.log 2>&1

# Function to count NNKs
run_count() {
    fasta="$1"
    echo $fasta
    python3 -u pythonfiles/count_NNK.py "$fasta"
}

export -f run_count

# identify motifs from oPool fasta files
#python3 -u pythonfiles/id_motifs.py A3_oPool_NNK.fasta

# count NNKs in test set
#python3 -u pythonfiles/count_NNK.py paired/fasta/nnk_motif_test_set.fasta id_motifs/A3_motifs.xlsx

# count NNKs in all sequences
#find paired/fasta -type f -name 'A3*.fasta' | parallel -j 16 run_count

# sort rows by position and columns by amino acid
#find nnk_count -type f -name 'A3*.xlsx' | parallel -j 16 'python3 -u pythonfiles/sort_count_file.py nnk_count/{/.}.xlsx'

# set out WT position
#python3 -u pythonfiles/set_out_wt.py nnk_count/A3_naive_S1_disp.xlsx

# count the number of sequences with 0, 1, and multiple motifs
#python3 -u pythonfiles/count_motifs.py
