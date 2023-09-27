# This module contains functions that checks the input FASTA file for format, content, and previous analysis done.
from collections import Counter
#import os
import re, sys
from Bio import SeqIO


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


def search_for_string(filepath, search_string):
    # search for occurrences of the string in the sequence and store here:
    found_seqs = []

    search_string = search_string.lower() 

    # open and parse the fasta file. 
    for record in SeqIO.parse(filepath, "fasta"):
        header = str(record.description)
        sequence = str(record.seq)

        # convert sequence to lower case for case-insensitive search
        sequence = sequence.lower()

        positions = []
        start_pos = 0
        while True:
            pos = sequence.find(search_string, start_pos)
            if pos == -1:
                break

            # store the position of the occurrence:
            positions.append(pos)

            # update the start position of next search:
            start_pos = pos + 1

        if positions:
            found_seqs.append({
                'record': header,
                'positions': positions
            })
    
    return found_seqs, search_string


# Write a function to reformat search results: 
def format_additional_results(additional_output_path, search_string, search_results):
    with open(additional_output_path, "w") as additional_report:
        output_str = 'Search Results for {} are shown here: '.format(search_string)
        additional_report.write(output_str)

        for result in search_results:
            header = result['record']
            positions = result['positions']

            additional_report.write(f"\nHeader: {header}\n")
            additional_report.write(f"Number of occurrences: {len(positions)}\n")
            additional_report.write("Positions: \n")

            for pos in positions:
                additional_report.write(str(pos) + "\n")
                
            additional_report.write("------------------\n")
  
def format_re_results(enzyme_names, positions_list, frags_list, new_header):

        output = f"{new_header}\n"

        # Iterate over each enzyme and its corresponding positions and fragments
        if isinstance(enzyme_names, (list,tuple)):
            for enzyme, pos_list, frags in zip(enzyme_names, positions_list, frags_list):  
                output += f"{enzyme}\n"
                for pos, frag in zip(pos_list, frags):
                    output += f"{pos}\n"
                    output += f"{frag}\n"
                output += "\n"
            output += "-------------------------\n"
        else:
            enzyme = enzyme_names
            pos_list = positions_list
            frags = frags_list
            output += f"{enzyme}\n"
            for pos, frag in zip(pos_list, frags):
                output += f"{pos}\n"
                output += f"{frag}\n"
            output += "--------------------------\n"
    
        return output
