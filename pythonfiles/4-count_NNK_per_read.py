import os
import pandas as pd
from Bio import SeqIO

# Directories
input_dir = "4_nnk_count/"
fasta_dir = "4_nnk_count/fasta_stratified_by_count/"
output_file = os.path.join(fasta_dir, "nnk_per_read_breakdown.xlsx")

# Results list
results = []

# Process each *_hypermut.fasta file
for filename in os.listdir(input_dir):
    if filename.endswith(".xlsx"):
        
        library = filename.replace(".xlsx", "")

        # Paths to stratified FASTA files
        file_0 = os.path.join(fasta_dir, f"{library}_0_nnk.fasta")
        file_1 = os.path.join(fasta_dir, f"{library}_1_nnk.fasta")
        file_multi = os.path.join(fasta_dir, f"{library}_multi_nnk.fasta")

        # Count sequences in each file (handle missing files gracefully)
        count_0 = len(list(SeqIO.parse(file_0, "fasta"))) if os.path.exists(file_0) else 0
        count_1 = len(list(SeqIO.parse(file_1, "fasta"))) if os.path.exists(file_1) else 0
        count_multi = len(list(SeqIO.parse(file_multi, "fasta"))) if os.path.exists(file_multi) else 0

        total = count_0 + count_1 + count_multi

        if total == 0:
            percent_0 = percent_1 = percent_multi = 0.0
        else:
            percent_0 = count_0 / total * 100
            percent_1 = count_1 / total * 100
            percent_multi = count_multi / total * 100

        results.append({
            "Library": library,
            "Total Reads": total,
            "0 NNK Reads": count_0,
            "1 NNK Reads": count_1,
            "Multi NNK Reads": count_multi,
            "0 NNK %": round(percent_0, 2),
            "1 NNK %": round(percent_1, 2),
            "Multi NNK %": round(percent_multi, 2),
        })

# Save to Excel
df = pd.DataFrame(results)
df = df.sort_values("Library")
df.to_excel(output_file, index=False)

print(f"Summary written to {output_file}")