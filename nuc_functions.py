# This module contains functions that analyzes nucleotide FASTA files. 

import re

def nuc_content(seq):
    a = len(re.findall('A',seq))
    t = len(re.findall('T',seq))
    c = len(re.findall('C',seq))
    g = len(re.findall('G',seq))
    n = len(re.findall('N',seq))
    gap = len(re.findall('-',seq))
    at = len(re.findall('AT',seq))  # This only counts instances of AT dinucleotide, not counts of A + counts of T
    gc = len(re.findall('GC',seq))  # This only counts instances of GC dinucleotide, not counts of G + counts of C
    return a,t,c,g,n,gap,at,gc

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
from Bio.SeqUtils import MeltingTemp as mt
from Bio.Seq import Seq

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

#BioPython has three different equations to find Tm
#Option 1 follows the 'Rule of thumb'.
#Option 2 uses empirical formulas based on GC content.
#Option 3 does calculation based on nearest neighbor thermodynamics
#Both options 2 and 3 could also take in salt and mismatch corrections as extra vairables for a more accurate measurement for those calculations (not included could be if we want to)
#seq = "AAGAGAGGAGACCCAACCACACAAGAGGTTGTCCTGGTTGC"
# print(cal_tm(seq,4))

