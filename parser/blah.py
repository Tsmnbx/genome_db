from Bio import SeqIO

# Concerns
# start for gene returned by biopython is off by one compared to genebank files???wtf
# start returned by biopython is -1. perhaps it wants to mark after which base to start reading?


### printing location features
def is_WGS(genome):
    keywords = genome.annotations["keywords"][0]
    if ("WGS" in keywords):
        return True
    return False

def get_locus(genome):
    return genome.name

def get_species_name(genome):
    genus = genome.annotations["source"].split()[0]
    species = genome.annotations["source"].split()[1]
    name = genus + "_" + species
    return name

def get_subspecies(source):
    subspecies = source.qualifiers["sub_species"][0]
    return subspecies

def get_strain(source):
    strain = source.qualifiers["strain"][0]
    return strain

def get_taxon(source):
    taxon = int(source.qualifiers["db_xref"][0].split(":")[1])
    return taxon

def get_qualifier(CDS,qualifier):
    if (qualifier == "codon_start"):
        return int(CDS.qualifiers["codon_start"][0])
    elif (qualifier == "product"):
        return CDS.qualifiers["product"][0]
    elif (qualifier == "protein_id"):
        return CDS.qualifiers["protein_id"][0]
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


# list_recs = list(SeqIO.parse("abcd.gbff","genbank"))
# genome = list_recs[0]

# source = genome.features[0]
# CDS = genome.features[2]
#
# print (is_WGS(genome))
# print (get_species_name(genome))
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
# print (get_qualifier(CDS,"translation"))
