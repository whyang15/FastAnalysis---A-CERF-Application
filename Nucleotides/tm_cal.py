from Bio.SeqUtils import MeltingTemp as mt
from Bio.Seq import Seq

def cal_tm(seq,option):
    cal = 0
    match option:
        case 1:
           cal = mt.Tm_Wallace(seq)
        case 2:
            cal = mt.Tm_GC(seq)
        case 3:
            cal = mt.Tm_NN(seq)
        case defualt:
            print("Not an option")
    return round(cal,2)

#BioPython has three different equations to find Tm
#Option 1 follows the 'Rule of thumb'
#Option 2 uses empirical formulas baed on GC content.
#Option 3 does calculation based on nearest neighbor thermodynamics
#Both options 2 and 3 could also take in salt and mismatch corrections as extra vairables for a more accurate measurement for those calculations (not included could be if we want to)
seq = "AAGAGAGGAGACCCAACCACACAAGAGGTTGTCCTGGTTGC"
print(cal_tm(seq,4))
