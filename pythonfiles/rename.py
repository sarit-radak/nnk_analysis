#!/usr/bin/env python3
import os
import pandas as pd
import sys

# Input Excel file
excel_file = "barcodes.xlsx"
libraries_dir = "libraries"

def main():
    # Make sure barcodes file exists
    if not os.path.exists(excel_file):
        print(f"Error: {excel_file} not found.")
        sys.exit(1)

    # Read Excel file
    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        print(f"Error reading {excel_file}: {e}")
        sys.exit(1)

    # Expect columns: Barcode, Library Name
    if "Barcode" not in df.columns or "Library Name" not in df.columns:
        print("Error: Excel file must contain 'Barcode' and 'Library Name' columns.")
        sys.exit(1)

    # Create mapping dict
    barcode_map = dict(zip(df["Barcode"], df["Library Name"]))

    # Ensure libraries folder exists
    if not os.path.exists(libraries_dir):
        print(f"Error: {libraries_dir} directory not found.")
        sys.exit(1)

    # Go through each barcode and rename if folder exists
    for barcode, libname in barcode_map.items():
        old_path = os.path.join(libraries_dir, barcode)
        new_path = os.path.join(libraries_dir, libname)

        if os.path.exists(old_path):
            if os.path.exists(new_path):
                print(f"Warning: {new_path} already exists. Skipping {barcode}.")
            else:
                os.rename(old_path, new_path)
                print(f"Renamed {old_path} → {new_path}")
        else:
            print(f"Warning: {old_path} not found, skipping.")

if __name__ == "__main__":
    main()