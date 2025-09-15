from calendar import c
import sys
import shutil

def count_fasta_sequences(fasta_file):
    with open(fasta_file) as f:
        return sum(1 for line in f if line.startswith(">"))


print ("")
print("Removing short reads...")

library = sys.argv[1]
min_len = int(sys.argv[2])

input_fasta = f"libraries/{library}/{library}_all.fasta"
good_file = f"libraries/{library}/{library}_len_pass.fasta"
bad_file = f"libraries/{library}/{library}_len_fail.fasta"

if min_len == 0:
    shutil.move(input_fasta, good_file)
    open(bad_file, 'w').close()
    print(f"Renamed {input_fasta} to {good_file} and created empty {bad_file}")
    sys.exit(0)

with open(input_fasta, 'r') as infile, open(good_file, 'w') as good_out, open(bad_file, 'w') as bad_out:
    seq = ""
    header = ""
    
    for line in infile:
        line = line.strip()
        if line.startswith(">"):
            if seq and len(seq) >= min_len:
                good_out.write(header + "\n" + seq + "\n")
            elif seq:
                bad_out.write(header + "\n" + seq + "\n")
            header = line
            seq = ""
        else:
            seq += line
    
    if seq and len(seq) >= min_len:
        good_out.write(header + "\n" + seq + "\n")
    elif seq:
        bad_out.write(header + "\n" + seq + "\n")

pass_count = count_fasta_sequences (good_file)
fail_count = count_fasta_sequences (bad_file)

pass_rate = round( 100 * pass_count / (pass_count + fail_count), 1)
fail_rate = round( 100 * fail_count / (pass_count + fail_count), 1)

print (f"{pass_count} sequences >= {min_len}bp ({pass_rate}%)")
print (f"{fail_count} sequences < {min_len}bp ({fail_rate}%)")