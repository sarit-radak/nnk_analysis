#!/bin/bash
#SBATCH --job-name=pair
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=72:00:00
#SBATCH --output=logs/pair.out
#SBATCH --error=logs/pair.err

cd $SUBMIT_SLURM_DIR
#echo $SUBMIT_SLURM_DIR
module purge
module load fastqc
module load python/3.8.3
module load seqtk/1.4
cd /gpfs/home/sradak/25-06-02_Interface_L4
BBMERGE='bbmap/bbmerge.sh'

main_dir=/gpfs/home/sradak/25-06-02_Interface_L4
#mkdir -p $main_dir/paired
#mkdir -p $main_dir/paired/fasta


# unzip files
#find "$main_dir/raw_fastq/Project/" -type f -name '*.gz' -exec sh -c 'gunzip -c "$0" > "${0%.gz}"' {} \;


#merge reads
#find "$main_dir/raw_fastq/Project/" -type f -name "*_R1_001.fastq" | while read -r r1_file; do

#    dir=$(dirname "$r1_file")
#    base=$(basename "$r1_file")
#    sample_name=$(echo "$base" | sed 's/_R1_001.fastq//')
#    r2_file="${dir}/${sample_name}_R2_001.fastq"
    
#    out_merge="$main_dir/paired/fastq/${sample_name}_paired.fastq"
#    out_hist="$main_dir/paired/hist/${sample_name}.hist"
#    out_fa="$main_dir/paired/fasta/${sample_name}_paired.fasta"
    
#    out_unmerged_r1="$main_dir/paired/unmerged/${sample_name}_unmerged_R1.fastq"
#    out_unmerged_r1_fa="$main_dir/paired/unmerged/${sample_name}_unmerged_R1.fasta"
#    out_unmerged_r2="$main_dir/paired/unmerged/${sample_name}_unmerged_R2.fastq"
#    out_unmerged_r2_fa="$main_dir/paired/unmerged/${sample_name}_unmerged_R2.fasta"
    
#    echo "Processing $sample_name..."

#    /opt/applications/bbtools/39.96/bin/bbmerge.sh in1="$r1_file" in2="$r2_file" out="$out_merge" ihist="$out_hist" outu1="$out_unmerged_r1" outu2="$out_unmerged_r2"
#    seqtk seq -a "$out_merge" > "$out_fa"
#    seqtk seq -a "$out_unmerged_r1" > "$out_unmerged_r1_fa"
#    seqtk seq -a "$out_unmerged_r2" > "$out_unmerged_r2_fa"
   
#done


#python3 -u pythonfiles/pair_summary.py









# run fastqc on individual libraries
#find "$main_dir/fastq_output/Project/" -type f -name '*.fastq' -exec fastqc -t 8 -o "$main_dir/Fastq_fastqc" "{}" \;












#run fastqc on combined libraries
#output_dir=$project_dir

#a3_file="$output_dir/A3_All.fastq"
#b2m_file="$output_dir/B2M_All.fastq"

#> "$a3_file"
#> "$b2m_file"

#find "$project_dir" -type f -name '*.fastq' ! -name 'A3_All.fastq' ! -name 'B2M_All.fastq' | while read -r file; do
#    filename=$(basename "$file")
#    
#    if [[ $filename == A3*.fastq ]]; then
#        cat "$file" >> "$a3_file"
#    elif [[ $filename == B2M*.fastq ]]; then
#        cat "$file" >> "$b2m_file"
#    fi
#done

#fastqc -t 4 -o "$fastqc_dir" "$b2m_file"
#fastqc -t 4 -o "$fastqc_dir" "$a3_file"











#for i in $source_dir/*R1_001.fastq.gz; do
#    sample_name=$(basename $i _R1_001.fastq.gz)
#    $BBMERGE in1=$source_dir/${sample_name}_R1_001.fastq.gz \
#             in2=$source_dir/${sample_name}_R2_001.fastq.gz \
#             out=$main_dir/Paired/$sample_name.merge.fq \
#             ihist=$main_dir/Paired/$sample_name.hist
#    seqtk seq -a $main_dir/Paired/$sample_name.merge.fq > $main_dir/Paired/$sample_name.merge.fa
#done




# run seqtk and create qual scores
# for fq in $source_dir/*; do
#     sample_name=$main_dir/Fastq_fastqc/$(basename $fq .fastq.gz)
#     seqtk fqchk $fq > $sample_name.seqtk.txt
#     cat $sample_name.seqtk.txt | grep "ALL" | cut -f8 > $sample_name.qual.txt
# done