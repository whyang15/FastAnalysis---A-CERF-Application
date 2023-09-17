# This script will parse a FASTA file and determine the length of amino acid sequence, each amino acid content within a sequence, and the hydrophobic / hydrophilic content of sequence.

# import necessary modules
import os
import sys
import re
from collections import Counter

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


# write a function that checks whether file exists. #
def check_Fasta_exists():
    # search_path = "/Users/Wei-Hsien/Desktop/"         # this will have to be defined by GUI?
    search_path = os.getcwd()
    full_path = None    # initialize the full_path variable
    filename = None    # initialize the filename variable
    
    for subdir, dirs, files in os.walk(search_path):
        for file in files:
            filepath = subdir + os.sep + file
            extensions = (".txt", ".fasta", ".fa")
            #ADDITION
            if filepath.endswith(extensions) and file != "Quickstart.txt":
                full_path = filepath
                filename = os.path.basename(full_path)
                print(f"The path of {filename} is {full_path}")
                #return full_path
            #print(full_path)
                break

    # read input file:
    if full_path is not None:
        try:
            file = open(full_path, 'r')
            print(f"The {filename} file exists")
            return file, full_path
        except FileNotFoundError:
            print(f"The {filename} file does not exist.")
    else:
        print("No matching FASTA file found.")

    return None   # Return None if no file is found or can be opened.
    

    
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

def get_hydrophobic_counts(protein):
    #protein_length = len(protein)
    # Current hydrophobic aa set does not include ambigous base notation:  J (Leucine (L) or Isoleucine (I))
    hydrophobic_aa_set = {'A', 'F', 'G', 'I', 'L', 'M', 'P', 'V', 'W'}
    hydrophobic_count = sum(1 for aa in protein if aa in hydrophobic_aa_set)
    #hydrophobic_pct = round( hydrophobic_count / protein_length, 2)
    return hydrophobic_count

def get_hydrophilic_counts(protein):
    #protein_length = len(protein)
    ''' Current hydrophilic aa set does not include ambigous base notations:  B (Aspartic acid (D) or Asparagine (N)), 
    Z (Glutamic acid (E) or Glutamine (Q))
    '''
    hydrophilic_aa_set = {'C', 'D', 'E', 'H', 'K', 'N', 'Q', 'R', 'S', 'T', 'Y'}
    hydrophilic_count = sum(1 for aa in protein if aa in hydrophilic_aa_set)
    #hydrophilic_pct = round( hydrophilic_count / protein_length, 2)    
    return  hydrophilic_count


# Write function to add values in 2 different dictionaries together.
def add_dict_values(dict1, dict2):
    counter1 = Counter(dict1)
    counter2 = Counter(dict2)
    sum_counter = counter1 + counter2
    sum_counter_dict = dict(sum_counter)
    return sum_counter_dict


# Write function format into FASTA file:
# Format to Fasta:
def formatFasta(seq, new_header, filepath):
    header = ""
    file_name = filepath
    header = ">" + str(new_header) + "\n"
    # format seq to write 80 nt per line
    formatted_seq = ""
    formatted_seq += header
    for pos in range(0, len(seq), 80):
        formatted_seq += seq[pos:pos+80]+"\n"
    # print(formatted_seq)
    
    fasta = open(file_name, 'w')
    fasta.write(formatted_seq)
    fasta.close()

# Main function:
def primary(i):
    file, filepath = check_Fasta_exists()
    #print(file)
    #seqs = getFastaDict(file)
    fasta_dict = {}
    seqlen = 0
    hphobic = 0
    hphilic = 0
    tmp = {}
    seq_lines = ""
    #ADDITION (needed a blank value for aa_counts_new)
    aa_counts_new = 0
    for line in file:
        if line.startswith(">"):  # header line
            key = line.strip()
            #print(key)
            #fasta_dict[key] = ""
            #new_lines.append(new_header)  # add the new header
        else: 
            seq = line.strip().replace(" ", "")
            #print(seq)
            seq_lines += seq
            # calculate per sequence line:
            seqlen += len(seq)
            if is_dna_or_aa(seq, "nucleotides"):
                print("This is not a peptide sequence.")
            else:
                aa_counts_line = get_aa_counts(seq)
                tmp = add_dict_values(tmp, aa_counts_line)
                aa_counts_new = tmp
                hphobic += get_hydrophobic_counts(seq)
                hphilic += get_hydrophilic_counts(seq)
    print(seq_lines)
    
    hphobic_pct = round(hphobic / seqlen, 2)
    hphilic_pct = round(hphilic / seqlen, 2)
    ln = "seqlen = " + str(seqlen)
    aa = "aa counts = " + str(aa_counts_new)
    hl = "hphilic_pct = " + str(hphilic_pct)
    ho = "hphobic_pct = " + str(hphobic_pct)
    
    new_header_list = [key, "||", aa, ln,  hl, ho]
    new_header = ' '.join(new_header_list)
    print(new_header)

    results = "Analysis Results: \n" + ln + "\n" + aa + "\n" + hl + "\n" + ho + "\n"
    print (results)

    if i == True:
        # format new file and write to new FASTA.
        formatFasta(seq_lines, new_header, filepath)
        
    return results

###-----------------------------------------------------
#main()
