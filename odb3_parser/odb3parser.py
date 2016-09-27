def get_operon(tsv,id):
    ### returns the operon as a list of all its attributes
    ### passing 0 for id will return the header of tsv file
    return tsv[id].strip().split('\t')

def get_operon_koid(operon):
    ### returns the koid for the operon
    return operon[0]

def get_operon_species(operon):
    if (any(item == "subsp." for item in operon[1].split())):
        return operon[1].split("subsp.")[0]
    else:
        return operon[1]

def get_operon_subspecies(operon):
    if (any(item == "subsp." for item in operon[1].split())):
        return operon[1].split("subsp.")[1].strip()
    else:
        return None

def get_operon_name(operon):
    return operon[2]

def get_operon_genes(operon):
    ### returns gene list for the operon as a list
    return operon[3].split(',')

def get_operon_pmid(operon):
    return operon[4]

def get_operon_annotation(operon):
    if (len(operon)>5):
        return operon[5]
    else:
        return None
