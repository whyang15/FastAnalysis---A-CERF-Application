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
    
    
