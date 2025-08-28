#!/usr/bin/env python3
import argparse
import os
import re
import gzip
import pandas as pd


def open_maybe_gzip(path):
    """Open plain text or gzipped file safely."""
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    return open(path, "r")

def count_fastq_reads(file_path):
    """Count reads in a FASTQ file by counting every 4th line (header lines)."""
    count = 0
    with open_maybe_gzip(file_path) as f:
        for i, _ in enumerate(f):
            if i % 4 == 0:
                count += 1
    return count

def extract_library_name(filename):
    """
    From filename like:
    L4-1_B2M_TCR_S3_OT-1t_S29_L001_R1_001.fastq
    return:
    L4-1_B2M_TCR_S3_OT-1t
    """
    return re.sub(r"_S[0-9]+_L001_R1_001\.fastq(\.gz)?$", "", filename)

def process_demultiplex():
    base_dir = "1_raw_fastq/project"
    results = {}

    for subdir in sorted(os.listdir(base_dir)):
        subpath = os.path.join(base_dir, subdir)
        if not os.path.isdir(subpath):
            continue

        for fname in os.listdir(subpath):
            if fname.endswith("_R1_001.fastq") or fname.endswith("_R1_001.fastq.gz"):
                fpath = os.path.join(subpath, fname)
                libname = extract_library_name(fname)
                read_count = count_fastq_reads(fpath)
                results[libname] = read_count
                break  # only one R1 per dir
    return results

def update_summary(results, step_name):
    """Write results to summary.xlsx with pandas"""
    outfile = "summary.xlsx"

    if os.path.exists(outfile):
        df = pd.read_excel(outfile, index_col=0)
    else:
        df = pd.DataFrame()

    for lib, count in results.items():
        df.loc[lib, step_name] = count

    df.to_excel(outfile)

def count_fasta_reads(file_path):
    """Count reads in a FASTA file by counting '>' header lines."""
    count = 0
    with open_maybe_gzip(file_path) as f:
        for line in f:
            if line.startswith(">"):
                count += 1
    return count

def process_pair():
    base_dir = "2_paired/fasta"
    results = {}

    for fname in os.listdir(base_dir):
        fpath = os.path.join(base_dir, fname)
        if os.path.isdir(fpath) and fname == "first_1000":
            continue  # skip the first_1000 directory
        if fname.endswith(".fasta") or fname.endswith(".fasta.gz"):
            libname = re.sub(r"\.fasta(\.gz)?$", "", fname)
            read_count = count_fasta_reads(fpath)
            results[libname] = read_count
    return results

def process_len_cutoff():
    base_dir = "3_len_filtered"
    results = {}

    for fname in os.listdir(base_dir):
        fpath = os.path.join(base_dir, fname)
        if os.path.isdir(fpath):
            continue
        if fname.endswith(".fasta") or fname.endswith(".fasta.gz"):
            libname = re.sub(r"\.fasta(\.gz)?$", "", fname)
            read_count = count_fasta_reads(fpath)
            results[libname] = read_count
    return results

def process_count_nnk():
    base_dir = "4_nnk_count"
    results = {}

    for fname in os.listdir(base_dir):
        fpath = os.path.join(base_dir, fname)
        if os.path.isdir(fpath):
            continue
        if fname.endswith(".xlsx"):
            libname = re.sub(r"\.xlsx$", "", fname)
            
            # Load Excel file
            df = pd.read_excel(fpath, engine="openpyxl")
            
            # Find the "Total" row and sum all numeric values
            total_row = df[df.iloc[:,0] == "Total"]
            if not total_row.empty:
                read_count = total_row.iloc[0,1:].sum()
                results[libname] = int(read_count)
            else:
                results[libname] = 0
    return results

def main():
    parser = argparse.ArgumentParser(description="Count reads at various pipeline steps")

    parser.add_argument("-demultiplex", action="store_true", help="Process demultiplexed reads in 1_raw_fastq/project")
    parser.add_argument("-pair", action="store_true", help="Process paired reads in 2_pair/fasta")
    parser.add_argument("-len_cutoff", action="store_true", help="Process length-filtered reads in 3_len_filtered")
    parser.add_argument("-count_nnk", action="store_true", help="Process NNK count Excel files in 4_count_nnk")

    args = parser.parse_args()

    if args.demultiplex:
        results = process_demultiplex()
        update_summary(results, "Reads Demultiplexed")
    if args.pair:
        results = process_pair()
        update_summary(results, "Reads Paired")
    if args.len_cutoff:
        results = process_len_cutoff()
        update_summary(results, "Reads Past Length Cutoff")
    if args.count_nnk:
        results = process_count_nnk()
        update_summary(results, "Reads with NNKs Counted")

if __name__ == "__main__":
    main()