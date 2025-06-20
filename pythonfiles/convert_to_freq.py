import sys
import os
import pandas as pd

# Input file path from command line
input_file = sys.argv[1]

# Output file path
base, ext = os.path.splitext(input_file)
base = base.replace("nnk_count", "nnk_freq")
#base = base.replace ("_hypermut", "")
output_file = f"{base}{ext}"

# Read Excel sheet
df = pd.read_excel(input_file)

# List of amino acid columns (from * to Y)
aa_columns = df.columns[3:-1]  # exclude Motif, Sequence, Label and Total

# Frequency calculation
def calculate_frequencies(row):
    total = row["Total"]
    if total == 0:
        return pd.Series([0] * len(aa_columns), index=aa_columns)
    else:
        return row[aa_columns] / total

# Apply frequency calculation to each row
freq_df = df.copy()
freq_df[aa_columns] = df.apply(calculate_frequencies, axis=1)

# Save the result to a new Excel file
freq_df.to_excel(output_file, index=False)

print(f"Converted {input_file} to {output_file}")