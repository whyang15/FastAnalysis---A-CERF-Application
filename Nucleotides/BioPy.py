from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
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

with open("BioPy ORF Test","w") as file:
    #To Do: GC% for whole seq, Base count, Tm
    file_cont = list(SeqIO.parse("cat.fasta", "fasta"))
    for entry in range(len(file_cont)):
        seq_id = file_cont[entry].id
        sequence = file_cont[entry].seq
        revCompSeq = Seq(sequence).reverse_complement()
        
        for strand, working_seq in [('+',sequence), ('-', revCompSeq)]:
            working_seq = Seq(working_seq)
            for frame in range (3):
                seq_dic = coding_region_finder(working_seq,frame)
                count = 1
                for seq in seq_dic:

                    coding_seq = Seq(seq_dic[seq])
                    translated_seq = coding_seq.translate()

                    length_nt = len(coding_seq)
                    length_aa = len(translated_seq)
                    start = working_seq.index(coding_seq)+1
                    end = start + length_nt
                                        
                    file.write("ORF:{}_Strand:{}_#{}_StartPos:{}_EndPos:{}_Lenght(nt|aa):{}|{}\n"
                            .format(frame+1,strand,count,start,end,str(length_nt),str(length_aa)))
                    file.write(str(coding_seq) + '\n' + str(translated_seq) + '\n')
                    count +=1