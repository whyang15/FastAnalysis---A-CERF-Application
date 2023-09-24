# Main function:
# This script will parse a FASTA file and determine the length of amino acid sequence, 
# each amino acid content within a sequence, and the hydrophobic / hydrophilic content of sequence.

# import necessary modules
import sys
from collections import Counter
from Bio import SeqIO
from Bio.Restriction import * 
from Bio.Restriction.PrintFormat import PrintFormat
import os
import fasta_functions as ff
import aa_functions as aa
import nuc_functions as nuc


# Main function:
def main():
    search_results = []
    search_string = ""
    num_records = 0
    rec_num = 0
    
    new_header_sep = "ff output ["
    formatted_seq=""
    additional_results=""
    option_input=0
    re_results_output = ""

    if len(sys.argv) < 2:
        print("File path not provided.")
        return
    
    filepath = sys.argv[1]
    print("File path: ", filepath)

    # Search Analysis:
    # Search is optional.  
    # If more occurrences are found, add to the positions list.
    search_results = ff.search_for_string(filepath)

    # specify your output directory for search and additional analysis results here.
    additional_results = filepath.rsplit(".",2)[0]
    additional_results_filename = additional_results + "_addtional_results.txt"
    additional_output_path = os.path.join("/Users/Wei-Hsien/Desktop", additional_results_filename)
    print(additional_output_path)

    
    # Check whether this FASTA file has already gone through CERF Fasta analysis:
    is_modified = ff.check_fasta_modified(filepath)
    if is_modified:
        
        search_results, search_string = ff.search_for_string(filepath)
        # open and save results to separate file. 
        ff.format_additional_results(additional_output_path, search_string.upper(), search_results)
        return
    
    else:
        # continue with CERF Fasta analysis:
        # open FASTA file and read in as file:
        with open(filepath, "r") as file:

            # Ask user if they want to get Tm information.
            tm_input=input("Do you want Melting Temperature information? y/n ")
            if tm_input=="y".lower():
                print("BioPython has three different equations to find Tm: \n ")       
                print("Option 1 follows the 'Rule of thumb'. \n ")
                print("Option 2 uses empirical formulas based on GC content. \n ")
                print("Option 3 does calculation based on nearest neighbor thermodynamics. \n")
                print("NOTE:  The Tm calculations are based on default parameters. \n")
                print("This calculation does not take into account DNA/DNA, DNA/RNA, RNA/RNA and salt or chemical additives conditions ")
                option_input=input("Please choose a Tm calculation option: \n")
            else:
                tm = 0
                print("will not calculate Tm.")

            # Ask user if they want to get restriction enzyme cut sites information:
            # find all restriction enzyme sites?
            re_all_input = input("Search for restriction enzyme cut sites? y/n ")
            if re_all_input=="y".lower():
                print("You can enter a list of restriction enzymes to search for, or look through restriction enzyme database (All or Common).")
                print(" 'All' will look for restriction enzyme cut sites of all enzymes in database.")
                print(" 'Common' will look for restriction enzyme cut sites of commonly used restriction enzymes.")
                    
                re_batch_input = input("Enter list of retricton enzymes separated by ','. Use correct RE naming convention. Or enter 'All', or 'Common': ")
            else:
                re_all_input=="n".lower()
                print("will not do restriction enzyme searches.")   
            
            # get number of records in FASTA file.
            num_records = ff.get_num_records(filepath)  
            
            # parse each record.  
            for record in SeqIO.parse(file, "fasta"):
                header = record.description
                print("current header:  ", header)
                
                # continue with aa or dna analysis if not modified:
                seq=str(record.seq)
                seqlen=len(seq)
                rec_num += 1
                new_header=""
                print("length of sequence is: ", str(seqlen))

                # check whether FASTA contains nucleotides or amino acids.  then proceed with correct analysis.
                if ff.is_dna_or_aa(seq, "nucleotides"):
                    print("This is a nucleotide sequence.")
                    nuc_counts = nuc.get_dna_counts(seq)
                    print(nuc_counts)

                    # records and base counts:
                    rc = "record_num="+str(rec_num)+"/"+str(num_records)
                    print(rc)
                    ln = "seqlen=" + str(seqlen)
                    nuccounts = "base_counts=" + str(nuc_counts)
                    at_pct = round(nuc.get_at_counts(seq) / seqlen, 1)
                    gc_pct = round(nuc.get_gc_counts(seq) / seqlen, 1)
                    at = "AT%=" + str(at_pct*100)
                    gc = "GC%=" + str(gc_pct*100)
                    
                    # calculate tm:
                    tm = nuc.cal_tm(seq, option_input)
                    opts={'1':'tm_wallace', '2':'tm_GC', '3':'tm_NN'}
                    opt=opts.get(option_input)

                    if tm != 0:
                        tm_string = "Tm(" + opt + ")=" + str(tm) + "'C"
                        new_header_list = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc, tm_string]
                    else:
                        new_header_list = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc]
                    
                    new_header = ' '.join(new_header_list)
                    print(new_header)
                    
                    # format new file and write to new FASTA.
                    formatted_seq += ff.formatFasta(seq, new_header)

                    # restriction enzyme digests:
                    if re_all_input == "y".lower():
                        
                        enzyme_names, positions_list, frags_list = nuc.reCut(seq, re_batch_input)
                        
                        # accumulate the formatted results:
                        re_results_output += ff.format_re_results(enzyme_names, positions_list, frags_list, new_header)

                        # specify output file name:
                        re_results_filename = filepath.rsplit(".",2)[0] + "_reCut_results.txt"
                        re_output_path = os.path.join("/Users/Wei-Hsien/Desktop", re_results_filename)
                        print(re_output_path)

                        #with open(re_output_path, "a") as re_output_file:
                          #  re_output_file.write(re_results_output)
                    
                    else:
                        print("No restriction enzyme cut site search.")

                else:
                    print("This is a peptide sequence.")
                    aa_counts_line = aa.get_aa_counts(seq)
                    hphobic += aa.get_hydrophobic_counts(seq)
                    hphilic += aa.get_hydrophilic_counts(seq)

                    hphobic_pct = round(hphobic / seqlen, 1)
                    hphilic_pct = round(hphilic / seqlen, 1)
                    rc = "record_num="+str(rec_num)+"/"+str(num_records)

                    ln = "seqlen=" + str(seqlen)
                    aacounts = "aa counts=" + str(aa_counts_line)
                    hl = "hphilic%=" + str(hphilic_pct*100)
                    ho = "hphobic%=" + str(hphobic_pct*100)
                            
                    new_header_list = [header, "||", new_header_sep, rc, ln, aacounts, hl, ho, "]"]
                    new_header = ' '.join(new_header_list)
                    print(new_header)

                    # format new file and write to new FASTA.
                    formatted_seq += ff.formatFasta(seq, new_header)

        with open(re_output_path, "w") as re_output_file:
            re_output_file.write(re_results_output)

        with open(filepath, "w") as output_file:
            output_file.write(formatted_seq)
        
        # if search string is defined:
        # search_string = sys.argv[2]
        if search_string is not None:
            search_results, search_string = ff.search_for_string(filepath)
            #print(search_results)
    
    # specify your output directory for search and additional analysis results here.          
    ff.format_additional_results(additional_output_path, search_string.upper(), search_results)
                
            



###-----------------------------------------------------
main()



