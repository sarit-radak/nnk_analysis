#!/usr/bin/env python3
import sys
import os
import pandas as pd
from filelock import FileLock

def count_fasta_reads(fasta_path):
    """Count number of sequences in a fasta file (lines starting with '>')."""
    if not os.path.exists(fasta_path):
        return 0
    count = 0
    with open(fasta_path, "r") as f:
        for line in f:
            if line.startswith(">"):
                count += 1
    return count

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 -u pythonfiles/count_reads.py <library>")
        sys.exit(1)

    library = sys.argv[1]
    summary_file = "summary.xlsx"
    lock_file = summary_file + ".lock"

    # Define fasta files
    base_path = f"libraries/{library}"
    files = {
        "Total Reads": f"{base_path}/{library}_all.fasta",
        "Reads Past Length Filter": f"{base_path}/{library}_len_pass.fasta",
        "1 NNK": f"{base_path}/{library}_1_nnk.fasta",
        "0 NNK": f"{base_path}/{library}_0_nnk.fasta",
        "Multiple NNK": f"{base_path}/{library}_multi_nnk.fasta",
    }

    # Count reads
    counts = {col: count_fasta_reads(path) for col, path in files.items()}

    # Prepare row
    row = {
        "Library": library,
        **counts
    }

    # Lock access so only one process writes at a time
    with FileLock(lock_file, timeout=120):
        if os.path.exists(summary_file):
            df = pd.read_excel(summary_file)
        else:
            df = pd.DataFrame(columns=[
                "Library",
                "Total Reads",
                "Reads Past Length Filter",
                "1 NNK",
                "0 NNK",
                "Multiple NNK"
            ])

        # Update or append row
        if library in df["Library"].values:
            df.loc[df["Library"] == library, list(row.keys())] = list(row.values())
        else:
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

        # Save back to Excel
        df.to_excel(summary_file, index=False)

if __name__ == "__main__":
    main()