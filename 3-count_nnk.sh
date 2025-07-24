#!/bin/bash
#SBATCH --job-name=count_nnk
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --exclusive
#SBATCH --time=72:00:00
#SBATCH --output=logs/count_nnk.out
#SBATCH --error=logs/count_nnk.err

exec > logs/count_nnk.log 2>&1

# identify motifs from oPool fasta files
python3 -u pythonfiles/3-id_motifs.py A3_oPool_NNK.fasta 'GTAGACCTGAGGATAAAGTTACATTAACTTGTCATGTTCTCGGTTTCTATCCGGCAGACATTACTCTTACATGGCAACTTAATGGTGAAGAGTTGATTCAGGACATGGAGCTCACAGAGACGGTTCCTGCTGGAGACGGCACCTATCAGAAGTGGGCGTCCGTTGTTGTTCCACTTGGAAAAGAACAGTATTATACATGTCATGTTTATCATCAAGGATTACCAGAGCCTTTAACATTACGTTGGGAGCCGCCACCATCCACAGGAGGATCCGGAGGCGAACA'





# Function to count NNKs
run_count() {
    fasta="$1"
    python3 -u pythonfiles/3-count_NNK.py 4_id_motifs/A3_oPool_NNK_motifs.xlsx "$fasta"
}

export -f run_count

# count NNKs in test set
#python3 -u pythonfiles/4-count_NNK.py 4_id_motifs/A3_oPool_NNK_motifs.xlsx 3_len_filtered/nnk_motif_test_set.fasta

# count NNKs in all sequences
#find 3_len_filtered -type f -name '*.fasta' | parallel -j 16 run_count

# sort rows by position and columns by amino acid
#find 5_nnk_count -type f -name '*.xlsx' | parallel -j 16 'python3 -u pythonfiles/5-sort_count_file.py 5_nnk_count/{/.}.xlsx'

# count the number of sequences with 0, 1, and multiple motifs
#python3 -u pythonfiles/6-count_motifs.py