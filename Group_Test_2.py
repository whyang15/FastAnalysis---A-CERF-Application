import re
def file_read():
    fileName =input("Please enter the name of the file that contains the sequence:")
    try:
        file = open(fileName, "r")
        fileCont = file.readlines()
        return fileCont
    except OSError:
        print("The file '{}' is not found.".format(fileName))
        return False

def seq_dictionary_generator(file_cont):
    
    header_position = []
    file_dictionary = {}
    
    for line in file_cont:
        if '>' in line:
            header_position.append(file_cont.index(line))
            
    for pos in header_position:
        file_dictionary[file_cont[pos]] = ' '.join(map(str,file_cont[pos+1:pos+2]))

    return file_dictionary
## Work in progress
def header_parser(header):
    modifiers =['acronym', 'altitude', 'anamorph', 'authority', 'bio-material', 'biotype', 'biovar', 'breed', 'cell-line', 'cell-type', 'chemovar', 'chromosome', 'clone', 'clone-lib', 'collected-by', 'collection-date', 'common', 'country', 'cultivar', 'culture-collection', 'dev-stage', 'ecotype', 'endogenous-virus-name', 'forma', 'forma-specialis', 'fwd-PCR-primer-name', 'fwd-PCR-primer-seq', 'genotype', 'group', 'haplogroup', 'haplotype', 'host', 'identified-by', 'isolate', 'isolation-source', 'lab-host', 'lat-lon', 'linkage-group', 'map', 'mating-type', 'note', 'organism', 'pathovar', 'plasmid-name', 'plastid-name', 'pop-variant', 'rev-PCR-primer-name', 'rev-PCR-primer-seq', 'segment', 'serogroup', 'serotype', 'serovar', 'sex', 'specimen-voucher', 'strain', 'sub-species', 'subclone', 'subgroup', 'substrain', 'subtype', 'synonym', 'teleomorph', 'tissue-lib', 'tissue-type', 'type', 'variety']
    mod_pos_index = {}
    temp = {}
    info = re.split(' ',header)
    for mod in modifiers:
        if mod in info:
            mod_pos_index[info.index(mod)] = mod
    mod_pos = sorted(mod_pos_index)
##    for pos in mod_pos:
##        data = info[pos+1:mod_pos[pos+1]]
##        temp[mod_pos_index.get(pos)] = data
    for pos in range(len(mod_pos)):
        if (pos+1) < len(mod_pos):
            data = info[mod_pos[pos]+1:mod_pos[pos+1]]
            temp[mod_pos_index.get(mod_pos[pos])] = data
        else:
            data = info[mod_pos[pos]+1::]
            temp[mod_pos_index.get(mod_pos[pos])] = data
    return temp
    
def number_of_entries_finder(dic):
    return len(dic)

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



def codon_generator(seq,working_frame):

    codon_list = ''
    final_valid_codon = len(seq)-2
    for codonStart in range(working_frame-1,final_valid_codon,3):
        codon = seq[codonStart:codonStart+3].upper()
        if len(codon.strip()) == 3:
            codon_list = codon_list + ' ' + codon
    return codon_list.lstrip()

def coding_region_finder(codon_list):
    stop_codons = ['TTA', 'TGA', 'TAG']
    start_positions = [pos for pos, start in enumerate(codon_list) if start == 'ATG']
    stop_positions = [pos for pos, stop in enumerate (codon_list) if stop in stop_codons]
    coding_regions = {}

    write = False
    temp_seq = ''
    count = 0
    for pos in range (0, len(codon_list), 4):
        codon = codon_list[pos:pos+3]
        if codon == 'ATG':
            write = True
        if write == True:
            temp_seq = temp_seq + ' ' + codon
        if codon in stop_codons:
            write = False
            coding_regions[count] = temp_seq.lstrip()
            temp_seq = ''
            count += 1
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
    for pos in range (0, len(codon_list),4):
        codon = codon_list[pos:pos+3]
        amino_acid = amino_code.get(codon, 'X')
        prot_sequence = prot_sequence + amino_acid
    return prot_sequence


seq_dictionary = seq_dictionary_generator(file_read())
print('Number of Entries in File: {}'.format(number_of_entries_finder(seq_dictionary)))
for key in seq_dictionary:
    header_info = header_parser(key)
    print(header_info)
    dna = seq_dictionary[key]
    dna_contents = dna_content(dna)
    print('The sequence length is {} bp\nThe number of A is {}\nThe number of T is {}\nThe number of G is {}\nThe number of C is {}\nThe number of AT paris is {}\nThe number of GC pairs is {}'
          .format(dna_length(dna),dna_contents[0],dna_contents[1],dna_contents[2],dna_contents[3],dna_contents[4],dna_contents[5]))
    rsDNA = reverse_strand(dna)
    csDNA = complement_strand(dna)
    rcsDNA = reverse_complement_strand(dna)

    print('DNA: ' + dna)
    print('Reverse: ' + rsDNA)
    print('Complement: ' + csDNA)
    print('Reverse Complement: ' + rcsDNA)

    for frame in range (3):
        print('Framework: {}'.format(frame+1))
        print()
        c = codon_generator(dna,frame)
        print('Sequence spaced out by codons')
        print(c)
        print()
        print('Coding Region Sequence')
        coding_region = coding_region_finder(c)
        for seq in coding_region:
            coding_seq = coding_region[seq]
            if coding_seq != '':
                print('Sequence Name/ID: {}'.format(seq))
                print(coding_seq)
                print()
        print('Protein Sequence for whole region:')
        print(protien_sequence_generator(c))
        print()
        print('Protein Sequence for coding regions:')
        for seq in coding_region:
            coding_seq = coding_region[seq]
            if coding_seq != '':
                print('Sequence Name/ID: {}'.format(seq))
                print(protien_sequence_generator(coding_seq))
                print()
