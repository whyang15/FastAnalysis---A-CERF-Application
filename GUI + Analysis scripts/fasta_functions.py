# This module contains functions that checks the input FASTA file for format, content, and previous analysis done.
from collections import Counter
#import os
import re


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
""" def check_Fasta_exists(filename):
    # search_path = "/Users/Wei-Hsien/Desktop/"         # this will have to be defined by GUI?
    if len(sys.argv) < 2:
        print("File path not provided.")
        return
    
    search_path = sys.argv[1]
    full_path = None    # initialize the full_path variable
    filename = None    # initialize the filename variable
    
    for subdir, dirs, files in os.walk(search_path):
        for file in files:
            filepath = subdir + os.sep + file
            extensions = (".txt", ".fasta", ".fa")
            if filepath.endswith(extensions):
                full_path = filepath
                filename = os.path.basename(full_path)
                print(f"The path of {filename} is {full_path}")

                break

    # read input file:
    if full_path is not None:
        try:
            #file = open(full_path, 'r')
            print(f"The {filename} file exists")
            return full_path
        except FileNotFoundError:
            print(f"The {filename} file does not exist.")
    else:
        print("No matching FASTA file found.")

    return None   # Return None if no file is found or can be opened. """


# Write function to add values in 2 different dictionaries together.
def add_dict_values(dict1, dict2):
    counter1 = Counter(dict1)
    counter2 = Counter(dict2)
    sum_counter = counter1 + counter2
    sum_counter_dict = dict(sum_counter)
    return sum_counter_dict


# Write function format into FASTA file:
# Format to Fasta:
def formatFasta(seq, new_header):
    header = ""
    header = ">" + str(new_header) + "\n"
    
    # format seq to write 80 nt per line
    formatted_seq = ""
    formatted_seq += header
    for pos in range(0, len(seq), 80):
        formatted_seq += seq[pos:pos+80]+"\n"
    # print(formatted_seq)
    formatted_seq += "\n"
    return formatted_seq

    #fasta = open(file_name, 'w')
    #fasta.write(formatted_seq)
    #fasta.close()


  
