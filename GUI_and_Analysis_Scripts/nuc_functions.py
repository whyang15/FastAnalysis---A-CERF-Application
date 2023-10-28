# This module contains functions that analyzes nucleotide FASTA files. 

import re
from Bio.SeqUtils import MeltingTemp as mt
from Bio.Seq import Seq
from Bio.Restriction import *

def get_dna_counts(seq):
    ''' Nucleotide code list currently does not include rare or ambigous bases: 
    R ( A or G), Y (C or T), S (G or C), W (A or T), K (G or T), M (A or C), B (C or G or T),
    D (A or G or T), H (A or C or T), V (A or C or G)  
    '''
    nuc_list = ['A', 'C', 'G', 'T', 'U', 'N', '.', '-']
    # Generate key:value (nucleotide:counts) in the nuc_count dictionary.
    nuc_count_dict = {nuc: seq.count(nuc) for nuc in nuc_list}
    return nuc_count_dict

def get_at_counts(seq):
    at_count = len(re.findall('A',seq)) + len(re.findall('T',seq))
    return at_count

def get_gc_counts(seq):
    gc_count = len(re.findall('G',seq)) + len(re.findall('C',seq))
    return gc_count

def cal_tm(seq, option):
    cal = 0
    
    if option=="Tm_Wallace":
        cal = mt.Tm_Wallace(seq)
    elif option == "Tm_GC":
        cal = mt.Tm_GC(seq)
    elif option == "Tm_NN":
        cal = mt.Tm_NN(seq)
    else:
        cal = 0

    return round(cal,2)

## Restriction Enzyme Cut Sites:
def reCut(sequence, rbatch):
    seq = Seq(sequence)
    rbatch_list = []  # initialize emptly list to store user input list of enzymes
    rb = []     # initialize empty list to store the rbatch as RestrictionBatch
    rbatch_list = rbatch.split(',')
    
    #regex allows user to enter "all" or "common" in any case
    search_ALL = re.findall('(?i)all', rbatch)
    search_COMMON = re.findall('(?i)common', rbatch)
    
    # if user want to input their list of restriction enzymes:
    if search_COMMON:
        cut_data = Analysis(CommOnly, seq)    # only enzymes that have a commercial supplier.
    elif search_ALL:
        cut_data = Analysis(AllEnzymes, seq)    # all enzymes in the REBASE database.
    else:
        print(rbatch)
        rb = RestrictionBatch(rbatch_list)      # initiate a restriction batch of enzymes.
        cut_data = Analysis(rb, seq)        # use only the enzymes in the restriction batch.
    
    enzyme_names = []       # initialize empty list to store enzyme names
    positions_list = []     # initialize empty list to store position names for each enzyme.
    frags_list = []         # initialize empty list to store fragments for each enzyme.

    for enz in cut_data.with_sites():
        try:
            enzyme_names.append(enz)
            #print(enzyme_names)
            positions_list.append(enz.search(seq))    # this is a list
            #print(positions_list)
            frags_list.append(enz.catalyse(seq))   # this is a list
            #print(frags_list)
            
        except:
            continue
    
    #return results_dict
    return enzyme_names, positions_list, frags_list

def coding_region_finder(codon_list,frame):
    stop_codons = ['TAA', 'TGA', 'TAG']     # This is list of STOP codons from the standard SGCO translation table from NCBI. 
    coding_regions = {}     # dictionary that saves the count and coding region sequence found in a frame. region 1:coding seq
    write = False
    temp_seq = ''
    count = 0
    for pos in range(frame, len(codon_list)-2, 3):
        codon = codon_list[pos:pos+3]
        if codon == 'ATG':
            write = True    # set write flag to true.
        if write == True:   # now that write is true, continue to add codons.
            temp_seq += codon
        if codon in stop_codons:    # if codon encountered is a stop codon, write is turned to false.
            write = False
            if len(temp_seq)>30:         # if template length is > 30 bp as default.
                coding_regions[count] = temp_seq
                count += 1
            temp_seq = ''
    if temp_seq != '' and 'ATG' in temp_seq and len(temp_seq) > 30:
        coding_regions[count] = temp_seq
    return coding_regions

def find_orfs(seq):
    import nuc_functions

    start = 0
    end = 0
    length_nt = 0
    length_aa = 0
    orf_records = []
    orf_seq = ""

    revCompSeq = Seq(seq).reverse_complement()
    count = 1
    for strand, working_seq in [('+',seq), ('-', revCompSeq)]:
        working_seq = Seq(working_seq)
        for frame in range(3):
            seq_dict = nuc_functions.coding_region_finder(working_seq,frame)
            
            for seq in seq_dict:
                
                coding_seq = Seq(seq_dict[seq])
                translated_seq = coding_seq.translate()

                length_nt = len(coding_seq)
<<<<<<< HEAD
                length_aa = len(translated_seq) - 1    # length of translated sequence should not include stop codon.
                
                if strand == '+':
                    start = working_seq.index(coding_seq) + 1
                    end = start + length_nt - 1
                elif strand == '-':
                    start = len(working_seq) - working_seq.index(coding_seq)
                    end = len(working_seq) - (working_seq.index(coding_seq) + length_nt) + 1
                                 
                orf_string = "ORF{} Strand{} Frame{} StartPos:{} EndPos:{} Length(nt|aa):{}|{} \n".format(count,strand,frame+1,start,end,str(length_nt),str(length_aa))
=======
                length_aa = len(translated_seq)
                start = working_seq.index(coding_seq)+1
                end = start + length_nt
                                    
                orf_string = "ORF{} Strand{} ID{} StartPos:{} EndPos:{} Length(nt|aa):{}|{} \n".format(frame+1,strand,count,start,end,str(length_nt),str(length_aa))
>>>>>>> f3f6afef79915ad02d92d5bad65ecbdff4d9e992
                orf_seq = str(orf_string) + str(translated_seq) + "\n"
                                   
                count +=1

                orf_records.append(str(orf_seq))

    return list(set(orf_records))
