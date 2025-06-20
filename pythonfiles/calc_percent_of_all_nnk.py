import pandas as pd
import sys

# Get file path from command line
if len(sys.argv) != 2:
    print("Usage: python calc_percent_of_all_nnk.py <path_to_excel_file>")
    sys.exit(1)

input_file = sys.argv[1]
print (input_file)

# Read the Excel file
df = pd.read_excel(input_file)

# Ensure 'Total' column is numeric (sometimes Excel makes it object)
df['Total'] = pd.to_numeric(df['Total'], errors='coerce')

# Calculate sum of all totals
total_sum = df['Total'].sum()

# Avoid division by zero
if total_sum == 0:
    df["Percent of all NNK"] = 0
else:
    df["Percent of all NNK"] = df["Total"] / total_sum

# Save back to the same file
output_file = input_file.replace("nnk_freq", "nnk_percent_of_total")
df.to_excel(output_file, index=False)