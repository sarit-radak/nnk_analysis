#!/bin/bash
#SBATCH --job-name=calc_fc
#SBATCH --time=24:00:00
#SBATCH --output=logs/calc_fc.out
#SBATCH --error=logs/calc_fc.err

# convert counts to frequencies
find 5_nnk_count -maxdepth 1 -type f -name '*.xlsx' | parallel -j 16 'python3 -u pythonfiles/7-convert_to_freq.py'