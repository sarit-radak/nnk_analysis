import pandas as pd
import re
import sys

def add_wt_column(filepath, output_path):
    # Read the Excel file
    df = pd.read_excel(filepath)

    def get_wt_value(row):
        # Extract WT amino acid from the label
        match = re.search(r'(?:MHC|B2M)\s*([A-Z])', row['Label'])
        if match:
            wt_residue = match.group(1)
            return row.get(wt_residue, None)
        return None

    # Apply function to each row to extract WT count
    df['WT'] = df.apply(get_wt_value, axis=1)

    # Save to a new Excel file
    df.to_excel(output_path, index=False)

# Example usage
input_file = sys.argv[1]
add_wt_column(input_file, input_file.replace('.xlsx', '_wt_set_out.xlsx'))