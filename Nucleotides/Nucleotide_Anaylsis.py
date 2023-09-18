import re
def dna_length(seq):
    return len(seq)

def dna_content(seq):
    a = len(re.findall('A',seq))
    t = len(re.findall('T',seq))
    c = len(re.findall('C',seq))
    g = len(re.findall('G',seq))
    at = len(re.findall('AT',seq))
    gc = len(re.findall('GC',seq))
    return a,t,c,g,at,gc
       
def reverse_strand(seq):
    return seq[::-1].upper()

def complement_strand(seq):
    comp_strand = seq.replace('A','t').replace('T','a').replace('G','c').replace('C','g').upper()
    return comp_strand

def reverse_complement_strand(seq):
    rev_comp_strand = complement_strand(seq)
    rev_comp_strand = rev_comp_strand[::-1]
    return rev_comp_strand

def coding_region_finder(codon_list,frame):
    stop_codons = ['TAA', 'TGA', 'TAG']
    coding_regions = {}
    write = False
    temp_seq = ''
    count = 0
    for pos in range (frame, len(codon_list)-2, 3):
        codon = codon_list[pos:pos+3]
        if codon == 'ATG':
            write = True
        if write == True:
            temp_seq = temp_seq + codon
        if codon in stop_codons:
            write = False
            if len(temp_seq)>30:
                coding_regions[count] = temp_seq
                count += 1
            temp_seq = ''
    if temp_seq != '' and 'ATG' in temp_seq:
        coding_regions[count] = temp_seq
    return coding_regions    
def ctest(seq,frame):
    stop_codons = ['TTA', 'TGA', 'TAG']
    coding_regions = {}
    count = 1
    sequence = ''
    for base in range (frame, len(seq)-2,3):
        if seq[base:base+3] == 'ATG':
            if sequence !='':
                sequence = sequence + 'ATG'
            else:
                sequence = 'ATG'
        elif seq[base:base+3] in stop_codons:
            sequence = sequence + seq[base:base+3]
            if len(sequence) >= 30:
                coding_regions[count] = sequence
                count += 1
            sequence = ''     
        elif 'ATG' in sequence:
            sequence = sequence + seq[base:base+3]

    return coding_regions
def protien_sequence_generator(codon_list):
    amino_code = {
                'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
                'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
                'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
                'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
                'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
                'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
                'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
                'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
                'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
                'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
                'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
                'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
                'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
                'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
                'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
                'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W'}#Include unique fasta codes
    prot_sequence =''    
    for pos in range (0, len(codon_list),3):
        codon = codon_list[pos:pos+3]
        amino_acid = amino_code.get(codon, 'X')
        prot_sequence = prot_sequence + amino_acid
    return prot_sequence
