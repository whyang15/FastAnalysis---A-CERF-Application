# This script will parse a FASTA file and determine the length of amino acid sequence, each amino acid content within a sequence, and the hydrophobic / hydrophilic content of sequence.

# import necessary modules
import os
import argparse
import sys
import re

# pseudo code

''' write a function to read in FASTA.  This function reads in the entire sequence.
    It returns dnaseq if DNA, aaseq if Amino Acid. '''
def is_dna_or_aa(sequence, type):
    # define dictionary set:
    bases_dict = { 'nucleotides': re.compile('^[ACGTN]*$', re.I),
               'amino acids': re.compile('^[ACDEFGHIKLMNPQRSTVWY]*$', re.I)}
    
    # aa_characters = set("ACDEFGHIKLMNPQRSTVWY")
    if bases_dict.get(type).search(sequence) is not None:
        return True
    else:
        return False



def getSeq():
    search_path = "/Users/Wei-Hsien/Desktop/"         # this will have to be defined by GUI?
    filename = args.input
    print(filename)
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            file_path = os.path.join(root, filename)
            #print(file_path)
            print(f"The path of {filename} is {file_path}")

    # read input file:
    with open(file_path, 'r') as file:
        sequence = file.readlines()
        seq=""
    
        for line in sequence:
        # if line does not starts with ">", save as sequence for search:
            if line.startswith(">") == False:  # header line
                seq += line.strip().replace(" ", "")
                
        return seq 
    

# Define function that separates header from sequence in fasta file and store in dictionary. 
# Make function to generate dictionary of fastas:

def getFastaDict(sequence):
    fasta_dict = {}
    for line in sequence:
        if line.startswith(">"):
            match = re.search(r">([^\s]+)", line)
            if match:
                key = match.group().replace(">", "")
                fasta_dict[key] = ""
        # else, add to value in dictionary with \n removed:
        else:
            fasta_dict[key] += line.strip().replace(" ", "")
    print(fasta_dict.keys())
    return(fasta_dict.keys())



''' write a function to calculate length of sequence'''
def findLen(seq):
    seqlen = len(seq)
    return seqlen


''' write a function to calculate each amino acid content, then report the % hydrophobic / hydrophilic content'''
def get_aa_pct(protein):
    protein_length = len(protein)
    ''' AA code list currently does not include rare or ambigous bases:  B (Aspartic acid (D) or Asparagine (N)),
    J (Leucine (L) or Isoleucine (I)), O (Pyrrolysine), U (Selenocysteine), Z (Glutamic acid (E) or Glutamine (Q)), X (any)
    '''
    aa_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 
               'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y', '-', '*']
    # Generate key:value (amino acid:counts) in the aa_count dictionary.
    aa_count = {aa: protein.count(aa) for aa in aa_list}
    # Calculate the aa percentage using the count value for aa key from aa_count dict.
    # Append to aa_pct_dict dictionary
    aa_pct_dict = {aa: round(count / protein_length, 2) for aa, count in aa_count.items()}
    return aa_pct_dict

def get_aa_counts(protein):
    protein_length = len(protein)
    ''' AA code list currently does not include rare or ambigous bases:  B (Aspartic acid (D) or Asparagine (N)),
    J (Leucine (L) or Isoleucine (I)), O (Pyrrolysine), U (Selenocysteine), Z (Glutamic acid (E) or Glutamine (Q)), X (any)
    '''
    aa_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 
               'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y', '-', '*']
    # Generate key:value (amino acid:counts) in the aa_count dictionary.
    aa_count_dict = {aa: protein.count(aa) for aa in aa_list}
    return aa_count_dict

def get_hydrophobic_pct(protein):
    protein_length = len(protein)
    # Current hydrophobic aa set does not include ambigous base notation:  J (Leucine (L) or Isoleucine (I))
    hydrophobic_aa_set = {'A', 'F', 'G', 'I', 'L', 'M', 'P', 'V', 'W'}
    hydrophobic_count = sum(1 for aa in protein if aa in hydrophobic_aa_set)
    hydrophobic_pct = round( hydrophobic_count / protein_length, 2)
    return hydrophobic_pct

def get_hydrophilic_pct(protein):
    protein_length = len(protein)
    ''' Current hydrophilic aa set does not include ambigous base notations:  B (Aspartic acid (D) or Asparagine (N)), 
    Z (Glutamic acid (E) or Glutamine (Q))
    '''
    hydrophilic_aa_set = {'C', 'D', 'E', 'H', 'K', 'N', 'Q', 'R', 'S', 'T', 'Y'}
    hydrophilic_count = sum(1 for aa in protein if aa in hydrophilic_aa_set)
    hydrophilic_pct = round( hydrophilic_count / protein_length, 2)    
    return  hydrophilic_pct


# Main function:
def main(args):
    seq = getSeq()      
    seqlen=findLen(seq)
    print("sequence len is:  ", str(seqlen))
    if is_dna_or_aa(seq, "nucleotides") == True:
        print("This is not a peptide sequence.")
    else: 
        aa_counts = get_aa_counts(seq)
        print(aa_counts)
        #aa_pct = get_aa_pct(seq)
        #print(aa_pct)
        hphobic_pct = get_hydrophobic_pct(seq)
        print(f"hydrophobic aa pct: {hphobic_pct}")
        hphilic_pct = get_hydrophilic_pct(seq)
        print(f"hydrophilic aa pct: {hphilic_pct}")



###-----------------------------------------------------
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--input", help="input FASTA file")
    parser.add_argument("--output", help="output FASTA name")
    args=parser.parse_args()
    
    main(args)
