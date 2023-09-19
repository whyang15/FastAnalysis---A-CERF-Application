# import re
# def RE_Dictionary ():
#     reList = open("RestrictionEnzymes.txt").readlines()
#     reDic = {}
#     for RE in reList:
#         reData = RE.split(',')
#         reName = reData[0]
#         reTarget = reData[1].strip('\n')
#         reDic[reName] = reTarget
#     return reDic

# def RE_cut(seq):
#     reDic = RE_Dictionary()
#     count = 1
#     with open("cuts.txt","w") as file:
#         for enzyme in reDic:
#             pattern = str(reDic[enzyme]).replace('N','.')
#             file.write(enzyme + ':\t' + pattern)
#             matches = re.finditer(pattern.replace("'",""), seq)
#             cutSite = reDic[enzyme].find("'") 
#             cuts = []
#             for i in matches:
#                 cut = int((i.start()+ cutSite))
#                 cuts.append(cut)
#             if len(cuts) == 0:
#                 next
#             else:
#                 for i in cuts:
#                     print("There is a cut between positions {} and {}.".format(i,i+1))
#                     file.write(enzyme + '\n')
#                     file.write(str(count) + '\n')
#                     count +=1
#                     f1 =seq[0:i+1]
#                     f2=seq[i+1::]
#                     file.write(f1 + '\n')
#                     file.write(f2 + '\n')
from Bio.Restriction import *
from Bio.Seq import Seq

def reCut(sequence):
    seq = Seq(sequence)
    cut_data = Analysis(AllEnzymes, seq)

    for enz in cut_data.with_sites():
        try:
            print("{}\n{}".format(enz, enz.catalyse(seq)))
        except:
            continue

reCut("AAAGAGAGAGAAAGGAATAGCAAGACAGG")