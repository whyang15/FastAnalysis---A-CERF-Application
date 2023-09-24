# This module contains functions that analyzes nucleotide FASTA files. 

from Bio.SeqUtils import MeltingTemp as mt
from Bio.Seq import Seq
from Bio.Restriction import *
import re


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
    
# Utilizing built-in packages from BioPython, 
# write function to calculate melting temps for selected sequences.
# BioPython has three different equations to find Tm
# Option 1 follows the 'Rule of thumb'.
# Option 2 uses empirical formulas based on GC content.
# Option 3 does calculation based on nearest neighbor thermodynamics
# Both options 2 and 3 could also take in salt and mismatch corrections as extra 
#   vairables for a more accurate measurement for those calculations. 

# from Bio.SeqUtils import MeltingTemp as mt
# from Bio.Seq import Seq

def cal_tm(seq, option):
    cal = 0
    
    if option=="1":
        cal = mt.Tm_Wallace(seq)
    elif option == "2":
        cal = mt.Tm_GC(seq)
    elif option == "3":
        cal = mt.Tm_NN(seq, 3)
    else:
        print("Not an option")

    return round(cal,2)



## Restriction Enzyme Cut Sites:
#from Bio.Restriction import *
#from Bio.Seq import Seq

def reCut(sequence, rbatch='Common'):
    seq = Seq(sequence) 
    rbatch_list = []  # initialize emptly list to store user input list of enzymes
    rb = []     # initialize empty list to store the rbatch as RestrictionBatch
    rbatch_list = rbatch.split(',')
     # if user want to inut their list of restriction enzymes:
    if rbatch == "Common".lower():
        cut_data = Analysis(CommOnly, seq)    # only enzymes that have a commercial supplier.
    elif rbatch == "All".lower():
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



