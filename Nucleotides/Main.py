import Nucleotide_Anaylsis as na
import Working_With_Files as wwa

## Make it so that import works 
seq_dictionary = wwa.seq_dictionary_generator(wwa.file_read())
print('Number of Entries in File: {}'.format(wwa.number_of_entries_finder(seq_dictionary)))
for key in seq_dictionary:
    header_info = wwa.header_parser(key)
    print(header_info)
    dna = seq_dictionary[key]
    dna_contents = na.dna_content(dna)
    print('The sequence length is {} bp\nThe number of A is {}\nThe number of T is {}\nThe number of G is {}\nThe number of C is {}\nThe number of AT paris is {}\nThe number of GC pairs is {}'
          .format(na.dna_length(dna),dna_contents[0],dna_contents[1],dna_contents[2],dna_contents[3],dna_contents[4],dna_contents[5]))
    rsDNA = na.reverse_strand(dna)
    csDNA = na.complement_strand(dna)
    rcsDNA = na.reverse_complement_strand(dna)

    print('DNA: ' + dna)
    print('Reverse: ' + rsDNA)
    print('Complement: ' + csDNA)
    print('Reverse Complement: ' + rcsDNA)

    for frame in range (3):
        print('Framework: {}'.format(frame+1))
        print()
        c = na.codon_generator(dna,frame)
        print('Sequence spaced out by codons')
        print(c)
        print()
        print('Coding Region Sequence')
        coding_region = na.coding_region_finder(c)
        for seq in coding_region:
            coding_seq = coding_region[seq]
            if coding_seq != '':
                print('Sequence Name/ID: {}'.format(seq))
                print(coding_seq)
                print()
        print('Protein Sequence for whole region:')
        print(na.protien_sequence_generator(c))
        print()
        print('Protein Sequence for coding regions:')
        for seq in coding_region:
            coding_seq = coding_region[seq]
            if coding_seq != '':
                print('Sequence Name/ID: {}'.format(seq))
                print(na.protien_sequence_generator(coding_seq))
                print()