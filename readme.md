# nnk_analysis

This repo is designed to process illumina sequencing data from raw basecall values to counts of NNKs in each library.

To use this code:

1. Download or clone the repo to garibaldi

### `1-demultiplex_to_fastq.sh`

1. Copy the NextSeq data directory into the repo. It should have sub-directories **Autocenter, autofocus, etc. 
2. Add the library names and barcode indices to the sheet `barcodes.csv`
    1. “index” is the i7 adapter, “index2” is the reverse-complement of the i5 adapter.
    2. To find barcode identities:
        1. Download “[xGen for Illumina Index List](https://sfvideo.blob.core.windows.net/sitefinity/docs/default-source/supplementary-product-info/idt-master-index-list.xlsx?sfvrsn=8df8e307_12)” from [IDT’s website](https://www.idtdna.com/pages/products/next-generation-sequencing/workflow/xgen-ngs-library-preparation/ngs-adapters-indexing-primers/adapters-indexing-primers-for-illumina)
        2. Find sequences listed on “xGen UDI Primers Plate 1” sheet
3. Run the script

### `2-pair.sh`

1. Edit `main_dir` to reflect the project directory
2. Uncomment the code up to `python3 -u pythonfiles/1-pair_summary.py`
    
    I typically see pairing efficiencies between 50-80%. Reads from the naive and displaying sorts often pair less efficiently than the sorted libraries.
    
3. Uncomment only the code to extract the first 1000 sequences
4. Open these files in geneious
    1. Confirm that the reads align to the designed library
    2. Using the lengths graph tab, check the length distribution of paired reads
        1. Often, the naive and displaying libraries tend to be slightly messier
        2. There should be five peaks. These represent the distribution of read lengths that can be obtained by adding 0, 2, or 4 nt to either side of the amplicon
5. Set the length cutoff in the `filter()` function
6. Run the script with the final line uncommented

### `3-count_nnk.sh`

1. Upload the motif file to the project directory
    1. This file was created by [nnk_make](https://github.com/sarit-radak/nnk_make) during library design. It has the oligo names (”L4.1_A3_oPool0_R181”) and nucleotides framing the NNK (acccttttgNNKactgattct)
    2. It should be named “Lx_protein_motifs.xlsx”
2. Assemble a test set of sequences
    1. nnk_make already checks the oligos to confirm that the NNK motifs are unique. This step is done to confirm that any potentially contaminating DNA doesn’t have an NNK motif and that the motif identification and codon translation functions work.
    2. I typically copy-paste in each oligo in the oligopool then find + replace NNK for GGT. I also add other DNA that could potentially be contaminating my libraries (WT MHC sequences, etc…)
        1. Because K codes for G/T, this code won’t translate any codons that end in A or T because they are likely sequencing errors.
    3. The code expects for the test set as `3_len_filtered/nnk_motif_test_set.fasta`
    4. Modify the name of the motif file in this specific line
3. Count NNKs in the test set, confirm results are correct
4. Count NNKs in all libraries + number of NNKs per read
    1. I typically see ~50% of paired reads having exactly one NNK
    2. Reads with multiple NNKs are excluded from this analysis. They are likely generated when a polymerase aborts midway during amplification. This oligo, which already carries a mutation, then acts as a primer for a read with a different mutation. The final DNA fragment carries two NNKs. Because the amplification occurs when the libraries are pooled, we can’t deconvolute which library each mutation belongs to.
5. Check the biological replicates of the sorted libraries. Ensure the counts align with one another.