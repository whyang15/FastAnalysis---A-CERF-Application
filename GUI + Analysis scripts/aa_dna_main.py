# Main function:
# This script will parse a FASTA file and determine the length of amino acid sequence, 
# each amino acid content within a sequence, and the hydrophobic / hydrophilic content of sequence.

# import necessary modules
import os
import sys
import re
import pathlib
from collections import Counter
from Bio import SeqIO
from Bio.SeqUtils import MeltingTemp as mt

import fasta_functions as ff
import aa_functions as aa
import nuc_functions as nuc

#this function passes in the file from the GUI (which was either passed from the command line or uploaded by the user)
#the function returns modified: {whether the file has been previsouly analyzed}, message: {string describing whether the 
def pass_file(filepath):
    hphobic = 0
    hphilic = 0
    rec_num = 0
    num_records = 0
    new_header_sep = "ff output ["
    
    formatted_seq_Wallace=""
    formatted_seq_GC= ""
    formatted_seq_NN = ""
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
                return modified, message, formatted_seq_Wallace, formatted_seq_GC, formatted_seq_NN, formatted_seq
                break
            else:
                modified = False
                message = str("This file has not yet been analyzed")
            # continue with aa or dna analysis if not modified:
            seq=str(record.seq)
            seqlen=len(seq)
            rec_num += 1
            new_header=""
            print("length of sequence is: ", str(seqlen))

            if ff.is_dna_or_aa(seq, "nucleotides"):
                print("This is not a peptide sequence.")
                nuc_counts = nuc.get_dna_counts(seq)
                print(nuc_counts)

                rc = "record_num="+str(rec_num)+"/"+str(num_records)
                print(rc)
                ln = "seqlen=" + str(seqlen)
                nuccounts = "base_counts=" + str(nuc_counts)
                at_pct = round(nuc.get_at_counts(seq) / seqlen, 2)
                gc_pct = round(nuc.get_gc_counts(seq) / seqlen, 2)
                at = "AT%=" + str(at_pct)
                gc = "GC%=" + str(gc_pct)

                # calculate tm:
                header_TM_Wallace = "Tm(Tm_Wallace)= " + str(round(mt.Tm_Wallace(seq),2)) + "'C"
                header_TM_GC = "Tm(Tm_GC)= " + str(round(mt.Tm_GC(seq),2)) + "'C"
                header_TM_NN = "Tm(Tm_NN)= " + str(round(mt.Tm_NN(seq),2)) + "'C"

                headerlist_Wallace = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc, header_TM_Wallace]
                headerlist_GC = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc, header_TM_GC]
                headerlist_NN = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc, header_TM_NN]
                headerlist_WO_TM = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc]
                
                Wallace_header = ' '.join(headerlist_Wallace)
                GC_header = ' '.join(headerlist_GC)
                NN_header = ' '.join(headerlist_NN)
                new_header = ' '.join(headerlist_WO_TM)

                formatted_seq_Wallace += ff.formatFasta(seq, Wallace_header)
                formatted_seq_GC += ff.formatFasta(seq, GC_header)
                formatted_seq_NN += ff.formatFasta(seq, NN_header)
                formatted_seq += ff.formatFasta(seq, new_header)

                
                #print(Wallace_header, GC_header, NN_header, new_header)
                
                # format new file based on TM methods
##                formatted_seq_Wallace += ff.formatFasta(seq, Wallace_header)
##                formatted_seq_GC += ff.formatFasta(seq, GC_header)
##                formatted_seq_NN += ff.formatFasta(seq, NN_header)
##                formatted_seq += ff.formatFasta(seq, new_header)
                
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
        print(formatted_seq)
                    
    return modified, message, formatted_seq_Wallace, formatted_seq_GC, formatted_seq_NN, formatted_seq
    
def commit_results(filepath, data):
    myfile = open(filepath, 'w')
    myfile.write(data)
    myfile.close()

def searching(filepath, string):
    #this works on Windows only, potentially Mac?
    desktop = pathlib.Path.home()/'Desktop'
    count = 0

    #filepath is passed in from the GUI.
    #string will be the users search, passed in from the GUI
    search_results = []

    # specify your output directory for search and additional analysis results here.
    additional_results = os.path.basename(filepath)
    additional_results_filename = (os.path.splitext(additional_results)[0]) + "_addtional_results.txt"
    
    #include if/else statement to see whether a a file already exists, so files dont become overwritten every time a new search is performed?
    #This would allows users to perform multiple searches, and each search would have its own file.
    additional_output_path = os.path.join(desktop, additional_results_filename)
    #if a search has already been performed and a file has been written to the desktop, an new file with a +1 count in the name will be added to the desktop
    #work on bug
    if os.path.exists(additional_output_path):
        count += 1
        additional_results_filename = (os.path.splitext(additional_results)[0]) + "_" + str(count) +"_addtional_results.txt"
        additional_output_path = os.path.join(desktop, additional_results_filename)

    search_results, search_string = ff.search_for_string(filepath, string)
    ff.format_additional_results(additional_output_path, search_string.upper(), search_results)
    
    return additional_output_path
