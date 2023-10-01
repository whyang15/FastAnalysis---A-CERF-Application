# This module contains functions that analyzes amino acid sequences. 
import os
import sys
import re

''' write a function to calculate length of sequence'''
def findLen(seq):
    seqlen = len(seq)
    return seqlen


''' write a function to calculate each amino acid content, then report the % hydrophobic / hydrophilic content'''
def get_aa_pct(protein):
    protein_length = len(protein)
    ''' AA code list currently does not include rare or ambigous bases:  B (Aspartic acid (D) or Asparagine (N)),
    J (Leucine (L) or Isoleucine (I)), O (Pyrrolysine), U (Selenocysteine), Z (Glutamic acid (E) or Glutamine (Q)), X (any)
    '''
    aa_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 
               'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y', '-', '*']
    # Generate key:value (amino acid:counts) in the aa_count dictionary.
    aa_count = {aa: protein.count(aa) for aa in aa_list}
    # Calculate the aa percentage using the count value for aa key from aa_count dict.
    # Append to aa_pct_dict dictionary
    aa_pct_dict = {aa: round(count / protein_length, 2) for aa, count in aa_count.items()}
    return aa_pct_dict

def get_aa_counts(protein):
    protein_length = len(protein)
    ''' AA code list currently does not include rare or ambigous bases:  B (Aspartic acid (D) or Asparagine (N)),
    J (Leucine (L) or Isoleucine (I)), O (Pyrrolysine), U (Selenocysteine), Z (Glutamic acid (E) or Glutamine (Q)), X (any)
    '''
    aa_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 
               'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y', '-', '*']
    # Generate key:value (amino acid:counts) in the aa_count dictionary.
    aa_count_dict = {aa: protein.count(aa) for aa in aa_list}
    return aa_count_dict

def get_hydrophobic_counts(protein):
    #protein_length = len(protein)
    # Current hydrophobic aa set does not include ambigous base notation:  J (Leucine (L) or Isoleucine (I))
    hydrophobic_aa_set = {'A', 'F', 'G', 'I', 'L', 'M', 'P', 'V', 'W'}
    hydrophobic_count = sum(1 for aa in protein if aa in hydrophobic_aa_set)
    #hydrophobic_pct = round( hydrophobic_count / protein_length, 2)
    return hydrophobic_count

def get_hydrophilic_counts(protein):
    #protein_length = len(protein)
    ''' Current hydrophilic aa set does not include ambigous base notations:  B (Aspartic acid (D) or Asparagine (N)), 
    Z (Glutamic acid (E) or Glutamine (Q))
    '''
    hydrophilic_aa_set = {'C', 'D', 'E', 'H', 'K', 'N', 'Q', 'R', 'S', 'T', 'Y'}
    hydrophilic_count = sum(1 for aa in protein if aa in hydrophilic_aa_set)
    #hydrophilic_pct = round( hydrophilic_count / protein_length, 2)    
    return  hydrophilic_count
