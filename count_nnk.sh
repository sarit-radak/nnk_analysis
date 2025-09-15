#!/bin/bash
mkdir -p logs

# rename folders according to library identity
#python3 -u pythonfiles/rename.py > logs/rename.log 2>&1


libraries=($(find libraries -mindepth 1 -maxdepth 1 -type d -exec basename {} \;))

for library in "${libraries[@]}"; do
    log_file="logs/${library}_extract.log"
    {
        echo "Processing library: $library"

        # extract sequences to fasta
        #python3 -u pythonfiles/extract_to_fasta.py "$library"

        # extract first 1000 reads
        #awk '/^>/ {count++} count<=1000' libraries/$library/$library"_all.fasta" >  libraries/$library/$library"_1000.fasta"

        # sort out short reads
        #python3 -u pythonfiles/sort_by_len.py "$library" 350
        
        # count nnk motifs
        #python3 -u pythonfiles/count_NNK.py "$library"

        # count reads and save to summary file
        python3 -u pythonfiles/count_reads.py $library
        
    } >"$log_file" 2>&1 &

done

# wait for all backgrounded jobs to finish
wait

rm summary.xlsx.lock