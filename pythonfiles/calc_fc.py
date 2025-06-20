import pandas as pd
import numpy as np
import math
import sys
import os

# Arguments: path file1 file2
path = sys.argv[1]
output_dir = sys.argv[2]
file1, file2 = sys.argv[3:5]

# Full paths
file1_path = os.path.join(path, file1)
file2_path = os.path.join(path, file2)

# Load files
df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)

# Validate row identity
meta_cols = ['Motif', 'Sequence', 'Label']
if not df1[meta_cols].equals(df2[meta_cols]):
    raise ValueError("The rows do not match between the two files.")

# Get amino acid columns (from '*' to 'Y', excluding 'Total' and "Percent of all NNK")
aa_cols = df1.columns[3:-1] # drop out total column from the end

# Small pseudocount for zero numerator
pseudocount = 0.000001

# Initialize output DataFrame
output_df = df1[meta_cols].copy()

# Compute log2 fold change
for col in aa_cols:
    numerator = df2[col].astype(float)
    denominator = df1[col].astype(float)

    # Replace numerator 0s with pseudocount
    #numerator = numerator.replace(0, pseudocount) # only needed if taking log in next step

    # Compute fold change with condition: if denominator == 0, result = -1
    result = np.where((denominator == 0), np.nan, (numerator / denominator))
    
    output_df[col] = result

# Write output
output_file = os.path.join(output_dir, file2)
#output_file = os.path.join("a3_disp_troubleshoot/fc", file2)
output_df.to_excel(output_file, index=False)
print(f"fold change saved to {output_file}")