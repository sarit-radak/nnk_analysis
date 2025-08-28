#!/bin/bash
#SBATCH --job-name=pair
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --exclusive
#SBATCH --time=72:00:00
#SBATCH --output=logs/pair.out
#SBATCH --error=logs/pair.err

#SBATCH --partition=highmem

module purge
module load fastqc
module load python/3.8.3
module load seqtk/1.4

mkdir -p 2_paired/fastq/
mkdir -p 2_paired/hist/
mkdir -p 2_paired/fasta/
mkdir -p 2_paired/fasta/first_1000/
mkdir -p 2_paired/unmerged/
mkdir -p 3_len_filtered
mkdir -p logs

exec > logs/pair.log 2>&1

BBMERGE='bbmap/bbmerge.sh'
main_dir=/gpfs/home/sradak/25-08-20_L4.1_B2M_Analysis


#merge reads
#find "$main_dir/1_raw_fastq/project/" -type f -name "*_R1_001.fastq" | while read -r r1_file; do

#    dir=$(dirname "$r1_file")
#    base=$(basename "$r1_file")
#    sample_name=$(echo "$base" | sed 's/_R1_001.fastq//')
#    r2_file="${dir}/${sample_name}_R2_001.fastq"
    
#    out_merge="$main_dir/2_paired/fastq/${sample_name}_paired.fastq"
#    out_hist="$main_dir/2_paired/hist/${sample_name}.hist"
#    out_fa="$main_dir/2_paired/fasta/${sample_name}.fasta"
    
#    out_unmerged_r1="$main_dir/2_paired/unmerged/${sample_name}_unmerged_R1.fastq"
#    out_unmerged_r1_fa="$main_dir/2_paired/unmerged/${sample_name}_unmerged_R1.fasta"
#    out_unmerged_r2="$main_dir/2_paired/unmerged/${sample_name}_unmerged_R2.fastq"
#    out_unmerged_r2_fa="$main_dir/2_paired/unmerged/${sample_name}_unmerged_R2.fasta"
    
#    echo "Processing $sample_name..."

#    /opt/applications/bbtools/39.96/bin/bbmerge.sh in1="$r1_file" in2="$r2_file" out="$out_merge" ihist="$out_hist" outu1="$out_unmerged_r1" outu2="$out_unmerged_r2" -forcemerge=t
#    seqtk seq -a "$out_merge" > "$out_fa"
#    seqtk seq -a "$out_unmerged_r1" > "$out_unmerged_r1_fa"
#    seqtk seq -a "$out_unmerged_r2" > "$out_unmerged_r2_fa"
   
#done


#python3 -u pythonfiles/1-pair_summary.py

# extract the first 1000 sequences
#cd 2_paired/fasta
#for file in *.fasta; do
#    awk '/^>/ {n++} n<=1000' "$file" > "first_1000/${file%.fasta}.fasta"
#done

# filter out short reads
#filter () {
#    fasta="$1"
#    cutoff=340
#    python3 pythonfiles/2-filter_fasta_by_length.py $fasta $cutoff
#}
#export -f filter

#find 2_paired/fasta -type f -maxdepth 1 -name 'L4-1*.fasta' | parallel -j 16 filter


# count the reads passing the length cutoff (I think this can be calculated from the spreadsheet written when NNKs per read are counted)
#cd 3_len_filtered/
#find . -type f -name "*.fasta" | while read -r file; do
    # Get the base filename
#    filename=$(basename "$file")
    
    # Extract the library name
#    libname="${filename%.L001_fasta}"

    # Count number of sequences
#    count=$(grep -c '>' "$file")

    # Print result
#    echo -e "${libname}\t${count}"
#done
