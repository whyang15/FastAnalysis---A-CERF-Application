import re
def file_read():
    fileName =input("Please enter the name of the file that contains the sequence:")
    try:
        file = open(fileName, "r")
        fileCont = file.readlines()
        return fileCont
    except OSError:
        return "The file not found."
        

def seq_dictionary_generator(file_cont):
    
    header_position = []
    file_dictionary = {}
    
    for line in file_cont:
        if '>' in line:
            header_position.append(file_cont.index(line))

    pos2 = header_position[1::]
    pos2 = iter(pos2)
    for pos in header_position:
        if pos != header_position[-1]:
            pos3 = next(pos2)
            file_dictionary[file_cont[pos]] = ' '.join(map(str,file_cont[pos+1:pos3]))
        else:
            file_dictionary[file_cont[pos]] = ' '.join(map(str,file_cont[pos+1::]))

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