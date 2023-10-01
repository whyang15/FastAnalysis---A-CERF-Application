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
from Bio.Seq import Seq
from Bio.Restriction import * 
from Bio.Restriction.PrintFormat import PrintFormat
from Bio.SeqRecord import SeqRecord

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
        # get number of records in FASTA file.
        num_records = ff.get_num_records(filepath)  
        
        for record in SeqIO.parse(file, "fasta"):
            header = record.description
            if new_header_sep in header:
                modified = True
                message = str("This file has already been modified by CERF Fasta Analysis.")
                return modified, message, formatted_seq_Wallace, formatted_seq_GC, formatted_seq_NN, formatted_seq
                break
            else:
                modified = False
                message = str("This file has not yet been analyzed. ")
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
                #For sequences greater then 500 bps long, Tm will not be calculated to save computational time
                if seqlen<= 500:
                    header_TM_Wallace = "Tm(Tm_Wallace)= " + str(round(mt.Tm_Wallace(seq),2)) + "'C"
                    header_TM_GC = "Tm(Tm_GC)= " + str(round(mt.Tm_GC(seq),2)) + "'C"
                    header_TM_NN = "Tm(Tm_NN)= " + str(round(mt.Tm_NN(seq),2)) + "'C"

                    headerlist_Wallace = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc, header_TM_Wallace]
                    headerlist_GC = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc, header_TM_GC]
                    headerlist_NN = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc, header_TM_NN]
                else:
                    headerlist_Wallace = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc]
                    headerlist_GC = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc]
                    headerlist_NN = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc]
                    
                headerlist_WO_TM = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc]
                
                Wallace_header = ' '.join(headerlist_Wallace)
                GC_header = ' '.join(headerlist_GC)
                NN_header = ' '.join(headerlist_NN)
                new_header = ' '.join(headerlist_WO_TM)

                formatted_seq_Wallace += ff.formatFasta(seq, Wallace_header)
                formatted_seq_GC += ff.formatFasta(seq, GC_header)
                formatted_seq_NN += ff.formatFasta(seq, NN_header)
                formatted_seq += ff.formatFasta(seq, new_header)

                message =str('\n\n' + message + "This FASTA file contains nucleotides sequences. \nSelect a Tm method from the dropdown. If Tm is selected, Tm will be included in restriction enzyme search and committed data.")

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
                formatted_seq_Wallace = formatted_seq
                formatted_seq_GC = formatted_seq
                formatted_seq_NN = formatted_seq
                message = str('\n\n' + message + "This file contains protein sequences. Tm is not performed on protein FASTA files. \n\nIf a Tm is selected from the dropdown and the file contains amino acids sequences, Tm will not be included in the header.")
                    
    return modified, message, formatted_seq_Wallace, formatted_seq_GC, formatted_seq_NN, formatted_seq
    
def commit_results(filepath, data):
    myfile = open(filepath, 'w')
    myfile.write(data)
    myfile.close()

def make_results_folder(filepath, string, extension):
    
    #this should work on any OS (perk of using pathlib), but should test (so far works on Windows)
    #FastAnalysis Results folder will contian all results from all searches and ORF generations from the user
    folder = r'FastAnalysis_Results'
    desktop = pathlib.Path.home()/'Desktop'
    desktop_folder = os.path.join(desktop, folder)

    #if this is the first search ever performed, the desktop folder to hold the results needs to be created first.
    if os.path.exists(desktop_folder) == False:
        os.makedirs(desktop_folder)

    # specify your output directory for search and additional analysis results here.
    #Finds the basename of the file from the full path, this can then be included in the name of the file containing the search results
    additional_results = os.path.basename(filepath)

    #Each search will include the string searched for in the file name. If the same string is searched on the same file, the file will overwrite the existing files contents.
    #By including the searched string in the name, this should make the results more easily findable by CERF once a system has been developed for adding the results as an attachment.
    additional_results_filename = (os.path.splitext(additional_results)[0]) + "_" + string + extension
    additional_output_path = os.path.join(desktop_folder, additional_results_filename)

    return additional_output_path
    
    
def searching(filepath, string):
    #filepath is passed in from the GUI.
    #string will be the users search, passed in from the GUI
    #call method for creating the results folder if needed, returns full path of the file that results will be written to, will include the string in the file name
    extension = "_addtional_results.txt"
    additional_output_path = make_results_folder(filepath, string, extension)
    search_results = []

    search_results, search_string = ff.search_for_string(filepath, string)
    ff.format_additional_results(additional_output_path, search_string.upper(), search_results)

    #return path to result file, so user knows where it will be located
    return additional_output_path

def restriction_enzyme(filepath, string, tm_dropdown):
    #If nothing is entered in the search bar but the button is selected, then an error message will display to the user
    if string == "" or None:
        message = str("Sequence not entered: Enter a valid sequence to search.")
        return message
    
    #call method for creating the results folder if needed, returns full path of the file that results will be written to, will include the string in the file name
    extension = "_reCut_results.txt"
    additional_output_path = make_results_folder(filepath, string, extension)
    re_results_output = ""
    
    new_header_sep = "ff output ["
    rec_num = 0
    num_records = 0
    

    with open(filepath, "r") as file:
        # get number of records in FASTA file.
        num_records = ff.get_num_records(filepath)  
            
        #parse through the FASTA file using BioPython
        for record in SeqIO.parse(file, "fasta"):

            seq=str(record.seq)
            
            #restriction enzyme sites are only found on nucleotides sequences, if user has uploaded a FASTA file containing amino acid sequences will not continue.
            if ff.is_dna_or_aa(seq, "nucleotides"):
                
                header = record.description
                
                
                #if the file has already had it's header updated, then no need to perform the analysis to make the new header.
                #Can just use the existing header for the search results. This allows restriction enzyme sites to still be searched for, regardless of whether the file's header has been modified.
                if new_header_sep in header:
                    new_header = header
                else:
                
                    seqlen=len(seq)
                    nuc_counts = nuc.get_dna_counts(seq)
                    rec_num += 1
                    
                    #general base counts and calcs to be included in the header
                    rc = "record_num="+str(rec_num)+"/"+str(num_records)
                    ln = "seqlen=" + str(seqlen)
                    nuccounts = "base_counts=" + str(nuc_counts)
                    at_pct = round(nuc.get_at_counts(seq) / seqlen, 1)
                    gc_pct = round(nuc.get_gc_counts(seq) / seqlen, 1)
                    at = "AT%=" + str(at_pct*100)
                    gc = "GC%=" + str(gc_pct*100)

                    #tm calc, will be included automatically in the header data if a Tm method is selected in the dropdown menu
                    #if no selection is made or a "Tm_None" is selected, Tm will not be included in the reulsts file
                    #For sequences greater then 500 bps long, Tm will not be calculated to save computational time
                    if (tm_dropdown == "Tm_Wallace" or tm_dropdown == "Tm_GC" or tm_dropdown == "Tm_NN") and seqlen <=500:
                        tm = nuc.cal_tm(seq, tm_dropdown)
                        tm_string = "Tm(" + tm_dropdown + ")=" + str(tm) + "'C"
                        new_header_list = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc, tm_string]
                    else:
                        new_header_list = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc]
                    
                    new_header = ' '.join(new_header_list)

                #Restriction enzymes
                enzyme_names, positions_list, frags_list = nuc.reCut(seq, string)
                
                # accumulate the formatted results:
                re_results_output = re_results_output + ff.format_re_results(enzyme_names, positions_list, frags_list, new_header)

                #write the results of the search to the new file
                commit_results(additional_output_path, re_results_output)

                #return the location of the results (full path)
                message = str("The results of your search can be found at: " + additional_output_path)
                
            #restriction enzyme sites are only found on nucleotides sequences, if user has uploaded a FASTA file containing protein sequences will not search for protein seqs.
            else:
                message = str("File contains protein sequences. Restriction enzymes sites are found in nucleotide sequences.")
                return message
            
    return message

def calculate_ORFs(filepath, string, tm_dropdown):

    #call method for creating the results folder if needed, returns full path of the file that results will be written to, will include the string in the file name
    extension = "_ORF_results.txt"
    additional_output_path = make_results_folder(filepath, string, extension)
    all_orf_records = []
    orf_records =[]     # initialize empty record to store outputs.
    
    new_header_sep = "ff output ["
    rec_num = 0
    num_records = 0

    #turn into a seperate method?
    with open(filepath, "r") as file:

        # get number of records in FASTA file.
        num_records = ff.get_num_records(filepath)  
            
        #parse through the FASTA file using BioPython
        for record in SeqIO.parse(file, "fasta"):

            seq=str(record.seq)
            
            #restriction enzyme sites are only found on nucleotides sequences, if user has uploaded a FASTA file containing amino acid sequences will not continue.
            if ff.is_dna_or_aa(seq, "nucleotides"):
                
                header = record.description
                
                #if the file has already had it's header updated, then no need to perform the analysis to make the new header.
                #Can just use the existing header for the search results. This allows restriction enzyme sites to still be searched for, regardless of whether the file's header has been modified.
                if new_header_sep in header:
                    new_header = header
                else:
                
                    seqlen=len(seq)
                    print(seqlen)
                    nuc_counts = nuc.get_dna_counts(seq)
                    rec_num += 1
                    
                    #general base counts and calcs to be included in the header
                    rc = "record_num="+str(rec_num)+"/"+str(num_records)
                    ln = "seqlen=" + str(seqlen)
                    nuccounts = "base_counts=" + str(nuc_counts)
                    at_pct = round(nuc.get_at_counts(seq) / seqlen, 1)
                    gc_pct = round(nuc.get_gc_counts(seq) / seqlen, 1)
                    at = "AT%=" + str(at_pct*100)
                    gc = "GC%=" + str(gc_pct*100)

                    #tm calc, will be included automatically in the header data if a Tm method is selected in the dropdown menu
                    #if no selection is made or a "Tm_None" is selected, Tm will not be included in the reulsts file
                    #For sequences greater then 500 bps long, Tm will not be calculated to save computational time
                    if (tm_dropdown == "Tm_Wallace" or tm_dropdown == "Tm_GC" or tm_dropdown == "Tm_NN") and seqlen <=500:
                        tm = nuc.cal_tm(seq, tm_dropdown)
                        tm_string = "Tm(" + tm_dropdown + ")=" + str(tm) + "'C"
                        new_header_list = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc, tm_string]
                    else:
                        new_header_list = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc]
                    
                    new_header = ' '.join(new_header_list)

                #ORFs
                orf_records = nuc.find_orfs(seq)
                
                # accumulate the formatted results:
                orf_records_string = ">" + new_header + "\n" + "".join(orf_records)
                all_orf_records.append(orf_records_string)
                all_orf_records_string = "\n".join(all_orf_records)

                #write the results of the search to the new file
                commit_results(additional_output_path, all_orf_records_string)

                #return the location of the results (full path)
                message = str("The results of your search can be found at: " + additional_output_path)
                
            #ORFs are only found on nucleotides sequences, if user has uploaded a FASTA file containing protein sequences will not search for protein seqs.
            else:
                message = str("File contains amino acid sequences. ORFs are found in nucleotide sequences.")
                return message
            
    return message
