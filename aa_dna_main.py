# Main function:
# This script will parse a FASTA file and determine the length of amino acid sequence, 
# each amino acid content within a sequence, and the hydrophobic / hydrophilic content of sequence.

# import necessary modules
import sys
from collections import Counter
from Bio import SeqIO
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
    hphobic = 0
    hphilic = 0
    gc_pct = 0
    new_header_sep = "ff output ["
    formatted_seq=""
    additional_results=""

    if len(sys.argv) < 2:
        print("File path not provided.")
        return
    
    filepath = sys.argv[1]
    print("File path: ", filepath)

    # Search Analysis:
    # Search is optional.  
    # If more occurrences are found, add to the positions list.
    """ if len(sys.argv) < 2:
        print("No search word provided.")
        search_string = ""
    else:
        search_string = sys.argv[2] """
    
    search_results = ff.search_for_string(filepath)

    # specify your output directory for search and additional analysis results here.
    additional_results = filepath.rsplit(".",2)[0]
    additional_results_filename = additional_results + "_addtional_results.txt"
    additional_output_path = os.path.join("/Users/Wei-Hsien/Desktop", additional_results_filename)
    print(additional_output_path)

    
    # Check whether this FASTA file has already gone through CERF Fasta analysis:
    is_modified = ff.check_fasta_modified(filepath)
    if is_modified:
        # if search string is defined:
        search_results, search_string = ff.search_for_string(filepath)
        #print(search_results)

        # open and save results to separate file. 
        ff.format_additional_results(additional_output_path, search_string.upper(), search_results)
        return
    
    else: 
        # continue with CERF Fasta analysis:
        # open FASTA file and read in as file:
        with open(filepath, "r") as file:
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

                    rc = "record_num="+str(rec_num)+"/"+str(num_records)
                    print(rc)
                    ln = "seqlen=" + str(seqlen)
                    nuccounts = "base_counts=" + str(nuc_counts)
                    at_pct = round(nuc.get_at_counts(seq) / seqlen, 2)
                    gc_pct = round(nuc.get_gc_counts(seq) / seqlen, 2)
                    at = "AT%=" + str(at_pct)
                    gc = "GC%=" + str(gc_pct)

                    new_header_list = [header, "||", new_header_sep, rc, ln, nuccounts, at, gc]
                    new_header = ' '.join(new_header_list)
                    print(new_header)
                    # format new file and write to new FASTA.
                    formatted_seq += ff.formatFasta(seq, new_header)

                else:
                    print("This is a peptide sequence.")
                    aa_counts_line = aa.get_aa_counts(seq)
                    hphobic += aa.get_hydrophobic_counts(seq)
                    hphilic += aa.get_hydrophilic_counts(seq)

                    hphobic_pct = round(hphobic / seqlen, 2)
                    hphilic_pct = round(hphilic / seqlen, 2)
                    rc = "record_num="+str(rec_num)+"/"+str(num_records)

                    ln = "seqlen=" + str(seqlen)
                    aacounts = "aa counts=" + str(aa_counts_line)
                    hl = "hphilic%=" + str(hphilic_pct)
                    ho = "hphobic%=" + str(hphobic_pct)
                            
                    new_header_list = [header, "||", new_header_sep, rc, ln, aacounts, hl, ho, "]"]
                    new_header = ' '.join(new_header_list)
                    print(new_header)

                    # format new file and write to new FASTA.
                    formatted_seq += ff.formatFasta(seq, new_header)

       
        with open(filepath, "w") as output_file:
            output_file.write(formatted_seq)

        
        # if search string is defined:
       # search_string = sys.argv[2]
        search_results, search_string = ff.search_for_string(filepath)
        #print(search_results)
    
    # specify your output directory for search and additional analysis results here.          
    ff.format_additional_results(additional_output_path, search_string.upper(), search_results)
    


###-----------------------------------------------------
main()



