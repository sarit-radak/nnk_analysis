import pandas as pd
import numpy as np
import sys
import os

# Input file path
output_dir = sys.argv[1]
input_file = sys.argv[2]
df = pd.read_excel(input_file)

# Metadata columns
meta_cols = ['Motif', 'Sequence', 'Label']

# Amino acid columns (from '*' to 'Y')
aa_cols = df.columns[3:]

# Output DataFrame
output_df = df[meta_cols].copy()

# Iterate over each row
log10_fc_data = []

for _, row in df.iterrows():
    label = row['Label']

    # Extract WT amino acid from the label
    if "MHC " in label:
        wt_aa = label.split("MHC ")[1][0]
    elif "B2M " in label:
        wt_aa = label.split("B2M ")[1][0]
    else:
        raise ValueError(f"Unexpected label format: {label}")

    # Get WT value (if it's missing or 0, set to np.nan to avoid divide-by-zero)
    wt_value = row.get(wt_aa, np.nan)
    if pd.isna(wt_value) or wt_value == 0:
        wt_value = np.nan

    # Compute log10 fold change against WT
    fc_row = {}
    for aa in aa_cols:
        val = row[aa]
        try:
            val = float(val)
            if wt_value > 0:
                fc = np.log10(val / wt_value) if val > 0 else np.log10(1e-6 / wt_value)
            else:
                fc = np.nan
                
        except:
            fc = np.nan
        fc_row[aa] = fc
    log10_fc_data.append(fc_row)

# Add log10 fold change data to output DataFrame
fc_df = pd.DataFrame(log10_fc_data, columns=aa_cols)
output_df = pd.concat([output_df, fc_df], axis=1)

# Write the output file
output_filename = os.path.basename(input_file)
output_path = os.path.join(output_dir, output_filename)
output_df.to_excel(output_path, index=False)
print(f"Saved log10 fold change to {output_path}")