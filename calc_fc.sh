#!/bin/bash
#SBATCH --job-name=calc_fc
#SBATCH --nodes=1
#SBATCH --partition=gpu
#SBATCH --ntasks=16
#SBATCH --time=24:00:00
#SBATCH --output=logs/calc_fc.out
#SBATCH --error=logs/calc_fc.err

# convert counts to frequencies
#find nnk_count -type f -maxdepth 1 -name 'A3*.xlsx' | parallel -j 16 'python3 -u pythonfiles/convert_to_freq.py'

# calculate percent of all NNK (top graph)
#find nnk_freq -type f -maxdepth 1 -name 'A3*.xlsx' | parallel -j 16 'python3 -u pythonfiles/calc_percent_of_all_nnk.py'

# calculate FC against naive (fc1_vs_naive)
#python3 -u pythonfiles/calc_fc.py nnk_freq/ fc1_vs_naive/ A3_N_S1.xlsx A3_Pair_S1_Pool.xlsx
#python3 -u pythonfiles/calc_fc.py nnk_freq/ fc1_vs_naive/ A3_N_S1.xlsx A3_Pair_S2_S12.xlsx
#python3 -u pythonfiles/calc_fc.py nnk_freq/ fc1_vs_naive/ A3_N_S1.xlsx A3_TCR_S1_Pool.xlsx
#python3 -u pythonfiles/calc_fc.py nnk_freq/ fc1_vs_naive/ A3_N_S1.xlsx A3_TCR_S2_S17.xlsx
#python3 -u pythonfiles/calc_fc.py nnk_freq/ fc1_vs_naive/ A3_N_S1.xlsx A3_TCR_S3_mOT-1_S22.xlsx
#python3 -u pythonfiles/calc_fc.py nnk_freq/ fc1_vs_naive/ A3_N_S1.xlsx A3_TCR_S3_tOT-1_S23.xlsx


# calculate average frequency across four selection 1 display replicates
#python3 -u pythonfiles/average_disp.py nnk_freq/ A3_S1_Disp_a_S2.xlsx A3_S1_Disp_b_S3.xlsx A3_S1_Disp_c_S4.xlsx A3_S1_Disp_d_S5.xlsx A3_S1_Disp_a-d.xlsx

# calculate FC against S1 displaying average (fc1_vs_disp)
#python3 -u pythonfiles/calc_fc.py nnk_freq/ fc1_vs_disp/ A3_S1_Disp_a-d.xlsx A3_Pair_S1_Pool.xlsx
#python3 -u pythonfiles/calc_fc.py nnk_freq/ fc1_vs_disp/ A3_S1_Disp_a-d.xlsx A3_Pair_S2_S12.xlsx
#python3 -u pythonfiles/calc_fc.py nnk_freq/ fc1_vs_disp/ A3_S1_Disp_a-d.xlsx A3_TCR_S1_Pool.xlsx
#python3 -u pythonfiles/calc_fc.py nnk_freq/ fc1_vs_disp/ A3_S1_Disp_a-d.xlsx A3_TCR_S2_S17.xlsx
#python3 -u pythonfiles/calc_fc.py nnk_freq/ fc1_vs_disp/ A3_S1_Disp_a-d.xlsx A3_TCR_S3_mOT-1_S22.xlsx
#python3 -u pythonfiles/calc_fc.py nnk_freq/ fc1_vs_disp/ A3_S1_Disp_a-d.xlsx A3_TCR_S3_tOT-1_S23.xlsx

# calculate FC vs WT position
#find fc1_vs_naive -type f -maxdepth 1 -name 'A3*.xlsx' | parallel -j 16 'python3 -u pythonfiles/calc_fc_vs_wt.py fc2_vs_wt_naive'
#find fc1_vs_disp -type f -maxdepth 1 -name 'A3*.xlsx' | parallel -j 16 'python3 -u pythonfiles/calc_fc_vs_wt.py fc2_vs_wt_disp'