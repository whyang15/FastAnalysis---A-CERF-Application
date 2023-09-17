import Nucleotide_Anaylsis as na
import Working_With_Files as wwa

file1 = wwa.file_read()
seq_dictionary = wwa.test(file1)#wwa.seq_dictionary_generator(file1)
sum = 0
print('Number of Entries in File: {}'.format(wwa.number_of_entries_finder(seq_dictionary)))
count = 0
strand = '+'
##Note: Used the NIH ORF Finder as Reference. It included ORFs that had no stop codon and were located at the end of the sequnce
##          Do we still want to include those ORFs with no stop codons?
with open ("data_storage_test.txt","w") as file:
    for key in seq_dictionary:
        seq_id = str(key).split(' ')[0]
        file.write(seq_id)
        header_info = wwa.header_parser(key)
        dna = str(seq_dictionary[key])
        file.write('\n'+dna)
        file.write('\n'+na.reverse_complement_strand(dna))
        dna_contents = na.dna_content(dna)
        file.write('The sequence length is {} bp\nThe number of A is {}\nThe number of T is {}\nThe number of G is {}\nThe number of C is {}\nThe number of AT paris is {}\nThe number of GC pairs is {}'
            .format(na.dna_length(dna),dna_contents[0],dna_contents[1],dna_contents[2],dna_contents[3],dna_contents[4],dna_contents[5]))
        for frame in range (6):
            working_frame = frame
            match frame:
                case 3:
                    working_frame = 0
                    dna = na.reverse_complement_strand(dna)
                    strand = '-'
                case 4:
                    working_frame = 1
                case 5: 
                    working_frame = 2

            #Finds all the potential coding regions. Returns a dictionary
            coding_region = na.coding_region_finder(dna,working_frame)

            #Dictionary format {orf id: (nucelotide sequence),(amino acid sequence)}
            ORF_dictionary = {}
            
            #Loop through the dictionary
            for seq in coding_region:
                temp_gene_data = []
                coding_seq = coding_region[seq]
                #if coding_seq != '':
                temp_gene_data.append(coding_seq)
                temp_gene_data.append(na.protien_sequence_generator(coding_seq))
                #if temp_gene_data !=[]:
                ##Need to correct the postions of reverse strand orfs, have to be based on forward strand.
                orf_id ='\n'+ seq_id + '_ORF'+ str(frame+1) + '_Strand:' + strand + '_Gene' + str(seq) + '_StartPos:' + str(dna.index(temp_gene_data[0])+1) + '_StopPos:'+str(dna.index(temp_gene_data[0])+len(temp_gene_data[0]))+'_Len(bp):' + str(len(temp_gene_data[0])) + ',\n'
                ORF_dictionary[orf_id] = temp_gene_data
                file.write(orf_id)
                file.write('NulcSeq:' + temp_gene_data[0] + ',')
                file.write('ProtSeq:' + temp_gene_data[1] + ',')
                count +=1
            #New seq dictionary format
            #{header id : (sequence),{orf_id: (nucleotide sequence),(amino acid sequence)}}
            #seq_dictionary[key].append(ORF_dictionary)
    file.write('\n'+str(count))
    print(sum)