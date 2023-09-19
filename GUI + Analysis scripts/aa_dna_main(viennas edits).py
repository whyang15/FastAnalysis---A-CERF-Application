# Main function:
# This script will parse a FASTA file and determine the length of amino acid sequence, 
# each amino acid content within a sequence, and the hydrophobic / hydrophilic content of sequence.

# import necessary modules
import os
import sys
import re
from collections import Counter
from Bio import SeqIO

import fasta_functions as ff
import aa_functions as aa

#this function passes in the file from the GUI (which was either passed from the command line or uploaded by the user)
#the function returns modified: {whether the file has been previsouly analyzed}, message: {string describing whether the 
def pass_file(filepath, c):
    hphobic = 0
    hphilic = 0
    new_header_sep = "ff output ["
    formatted_seq=""

    modified = False
    message = 'file contents not valid'
    # check whether this FASTA file has already gone through CERF Fasta analysis:
    with open(filepath, "r") as file:
        for record in SeqIO.parse(file, "fasta"):
            header = record.description
            print("current header:  ", header)
            if new_header_sep in header:
                modified = True
                message = str("This file has already been modified by CERF Fasta Analysis.")
                return modified, message
                break
            else:
                modified = False
                message = str("This file has not yet been analyzed")
            # continue with aa or dna analysis if not modified:
            seq=str(record.seq)
            seqlen=len(seq)
            new_header=""
            print("length of sequence is: ", str(seqlen))

            if ff.is_dna_or_aa(seq, "nucleotides"):
                print("This is not a peptide sequence.")   
            else:
                aa_counts_line = aa.get_aa_counts(seq)
                hphobic += aa.get_hydrophobic_counts(seq)
                hphilic += aa.get_hydrophilic_counts(seq)

                hphobic_pct = round(hphobic / seqlen, 2)
                hphilic_pct = round(hphilic / seqlen, 2)
                ln = "seqlen=" + str(seqlen)
                aacounts = "aa counts=" + str(aa_counts_line)
                hl = "hphilic_pct=" + str(hphilic_pct)
                ho = "hphobic_pct=" + str(hphobic_pct)
                          
                new_header_list = [header, "||", new_header_sep, ln, aacounts, hl, ho, "]"]
                new_header = ' '.join(new_header_list)
                print(new_header)
                print(new_header_list)

                # format new file and write to new FASTA.
                formatted_seq += ff.formatFasta(seq, new_header)

        #will write back to file if commit button is selected
        if c == True:
            with open(filepath, "w") as output_file:
                    output_file.write(formatted_seq)
                    
        return modified, message
