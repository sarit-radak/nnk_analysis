import pandas as pd
import re
import sys

def extract_label(motif):
    """Extract label based on motif format."""
    # Dynamically extract the letter (last character in the motif string)
    letter = motif[-1] if motif[-1].isalpha() else ""
    
    if motif.startswith("L4_A3"):
        match = re.search(r'oPool_(\d+\.\d+)', motif)
        if match:
            number = float(match.group(1))
            return f"MHC {letter}{int(number) + 200}"
    elif motif.startswith("L4_B2M_oPool1"):
        match = re.search(r'oPool1_(\d+\.\d+)', motif)
        if match:
            number = float(match.group(1))
            return f"B2M {letter}{int(number)}"
    elif motif.startswith("L4_B2M_oPool2"):
        match = re.search(r'oPool2_(\d+\.\d+)', motif)
        if match:
            number = float(match.group(1))
            return f"B2M {letter}{int(number) + 42}"
    return motif

def extract_sort_key(motif):
    # Match new format: oPool followed by an integer and a float
    match = re.search(r'oPool(\d+)_(\d+\.\d+)', motif)
    if match:
        return (int(match.group(1)), float(match.group(2)))

    # Match original format: oPool_ followed by a float
    match = re.search(r'oPool_(\d+\.\d+)', motif)
    if match:
        return (0, float(match.group(1)))  # Use 0 to sort these before oPool1, oPool2, etc.

    return (float('inf'), float('inf'))  # Fallback for unmatched cases

def process_aa_count_file(filepath):
    # Read the Excel file
    df = pd.read_excel(filepath)

    # Create a new column with sort keys
    df['SortKey'] = df['Motif'].apply(extract_sort_key)

    # Create the label column
    df['Label'] = df['Motif'].apply(extract_label)

    # Sort by the sort key and drop the helper column
    df = df.sort_values('SortKey').drop(columns='SortKey')

    # Check number of rows
    filename = filepath.split("/")[-1]
    expected_rows = 79 if filename.startswith("A3") else 99 if filename.startswith("B2M") else None
    actual_rows = df.shape[0]

    if expected_rows and actual_rows != expected_rows:
        raise ValueError(f"{filename}: Expected {expected_rows} rows, found {actual_rows}")

    # Sort columns alphabetically, keeping '*' first and 'Total' last
    aa_order = ['*'] + sorted([aa for aa in df.columns if aa not in ['Motif', 'Sequence', '*', 'Total'] and len(aa) == 1]) + ['Total']
    final_columns = ['Motif', 'Sequence', "Label"] + aa_order
    df = df[final_columns]

    return df


file = sys.argv[1]

output_df = process_aa_count_file(file)

output_filename = file.replace (".xlsx", ".xlsx")

output_df.to_excel(output_filename, index=False)