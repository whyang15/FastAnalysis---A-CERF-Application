# This module contains functions that checks the input FASTA file for format, content, and previous analysis done.
from collections import Counter
import sys
import re
from Bio import SeqIO


# write function to get the number of records in a FASTA file.
def get_num_records(filepath):
    with open(filepath, "r") as file:
    # get number of records in FASTA file.
        records = list(SeqIO.parse(file, "fasta"))
        num_records = len(records)
        print(f"This fasta contains {num_records} records.")
        return num_records    


# parse each record.  determine whether record has been modified.
def check_fasta_modified(filepath):
    new_header_sep = "FA output["
    with open(filepath, "r") as file:
        for record in SeqIO.parse(file, "fasta"):
            header = record.description
            print("current header:  ", header)
            if new_header_sep in header:
                
                print("This file has already been modified by CERF Fasta Analysis.")
                return True
    return False       


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



# Write a function that searches each sequence for a string.
# Use sys.args[2] as the search string input.  search_string argument is optional.
def search_for_string(filepath, search_string=None):
    # search for occurrences of the string in the sequence and store here:
    found_seqs = []

    if search_string is None:
        if len(sys.argv) < 3:
            print("No search word provided.")
            search_string = ""
            return found_seqs, search_string
        else:
            search_string = sys.argv[2]
      
    # covert search string to lower case for case-insensitive search
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


# Write a function to reformat Restriction Enzyme cut sites results:
#def format_re_results(results_string, new_header, re_outfile):
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
        
        #with open(re_outfile, 'a') as file:
         #   file.write(output)
        return output

