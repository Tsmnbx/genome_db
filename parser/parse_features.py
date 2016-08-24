from Bio import SeqIO

# Concerns
# start for gene returned by biopython is off by one compared to genebank files???wtf
# start returned by biopython is -1. perhaps it wants to mark after which base to start reading?


### printing location features
def is_WGS(locus):
    keywords = locus.annotations["keywords"][0]
    if ("WGS" in keywords):
        return True
    return False

def get_locus_name(locus):
    return locus.name

def get_species_name(source):
    genus = source.qualifiers["organism"][0].split()[0]
    species = source.qualifiers["organism"][0].split()[1]
    name = genus + "_" + species
    return name

def get_subspecies(source):
    if ("sub_species" in source.qualifiers.keys()):
        subspecies = source.qualifiers["sub_species"][0]
        return subspecies
    else:
        return None

def get_strain(source):
    if ("strain" in source.qualifiers.keys()):
        strain = source.qualifiers["strain"][0]
        return strain
    else:
        return None

def get_sub_strain(source):
    if ("sub_strain" in source.qualifiers.keys()):
        sub_strain = source.qualifiers["sub_strain"][0]
        return sub_strain
    else:
        return None

def get_taxon(source):
    taxon = int(source.qualifiers["db_xref"][0].split(":")[1])
    return taxon

def get_qualifier(CDS,qualifier):

    if (qualifier == "codon_start"):
        return int(CDS.qualifiers["codon_start"][0])

    elif (qualifier == "product"):
        return CDS.qualifiers["product"][0]

    elif (qualifier == "gene"):
        if ("gene" in CDS.qualifiers.keys()):
            return CDS.qualifiers["gene"][0]
        else:
            return None

    elif (qualifier == "gene_synonym"):
        if ("gene_synonym" in CDS.qualifiers.keys()):
            return CDS.qualifiers["gene_synonym"]
        else:
            return None

    elif (qualifier == "locus_tag"):
        return CDS.qualifiers["locus_tag"][0]

    elif (qualifier == "EC_number"):
        if ("EC_number" in CDS.qualifiers.keys()):
            return CDS.qualifiers["EC_number"]
        else:
            return None

    elif (qualifier == "protein_id"):
        if ("protein_id" in CDS.qualifiers.keys()):
            return CDS.qualifiers["protein_id"][0]
        else:
            return None

    elif (qualifier == "function"):
        if ("function" in CDS.qualifiers.keys()):
            return CDS.qualifiers["function"][0].split(";")
        else:
            return None

    elif (qualifier == "note"):
        if ("note" in CDS.qualifiers.keys()):
            return CDS.qualifiers["note"][0].split(";")
        else:
            return None

    elif (qualifier == "Pfam"):
        if ("note" in CDS.qualifiers.keys()):
            for tag in CDS.qualifiers["note"][0].split(";"):
                if ("Pfam" in tag):
                    return tag
        else:
            return None

    elif (qualifier == "UniProt"):
        for ref in CDS.qualifiers["db_xref"]:
            if ("UniProt" in ref):
                return ref.split(":")[1].split(":")
        return None

    elif (qualifier == "GI"):
        for ref in CDS.qualifiers["db_xref"]:
            if ("GI" in ref):
                return int(ref.split(":")[1])
        return None

    elif (qualifier == "translation"):
        return CDS.qualifiers["translation"][0]

    else:
        print ("valid qualifiers: codon_start,locus_tag, product, protein_id, translation")
        exit(1)

def get_start(CDS):
    location = CDS.location
    start = int(str(location).split("[")[1].split(":")[0]) + 1
    return start

def get_end(CDS):
    location = CDS.location
    end = int(str(location).split("[")[1].split(":")[1].split("]")[0])
    return end

def get_strand(CDS):
    location = CDS.location
    strand = int(location.strand)
    return strand


# genome = list(SeqIO.parse("ecoli.gbff","genbank"))
# locus = genome[0]

# source = locus.features[0]
# CDS = locus.features[11]

# print (is_WGS(locus))
# print (get_species_name(locus))
#
# print (get_subspecies(source))
# print (get_strain(source))
# print (get_taxon(source))
#
# print (get_start(CDS))
# print (get_end(CDS))
# print (get_strand(CDS))
#
# print (get_qualifier(CDS,"codon_start"))
# print (get_qualifier(CDS,"product"))
# print (get_qualifier(CDS,"protein_id"))
# print (CDS)
# print (get_qualifier(CDS,"translation"))
