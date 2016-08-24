from Bio import SeqIO
from parse_features import *

file_name = "../../GCA_001686325.1_ER_SAN_1.0_genomic.gbff"

genome = list(SeqIO.parse(file_name,"genbank"))
first_locus = genome[0]

if is_WGS(first_locus):
    num_of_locus = len(genome)
else:
    num_of_locus = 1

num_of_locus = 1

for locus_id in range(0, num_of_locus):
    # looping through all locus
    locus = genome[locus_id]
    locus_name = get_locus_name(genome[locus_id])

    # source
    source = locus.features[0]
    # applying all functions related to getting info from source
    print(get_species_name(source))
    # get_subspecies(source)
    print(get_strain(source))
    # get_sub_strain(source)
    # get_taxon(source)

    # number of genes inside the locus, genome[locus]
    num_features = len(locus.features)
    for feature_id in range(1,num_features):
        # if it is a CDS
        if (locus.features[feature_id].type == "CDS"):
            CDS = locus.features[feature_id]
            # applying all functions related to getting info from the CDS
            # get_qualifier(CDS, "gene")
            # get_qualifier(CDS, "gene_synonym")
            # get_qualifier(CDS, "locus_tag")
            # get_qualifier(CDS, "codon_start")
            # get_qualifier(CDS, "EC_number")
            # get_qualifier(CDS, "protein_id")
            # get_qualifier(CDS, "Pfam")
            # get_qualifier(CDS, "UniProt")
            # get_qualifier(CDS, "GI")
            # get_qualifier(CDS, "product")
            # get_qualifier(CDS, "translation")
            # get_qualifier(CDS, "function")
            # get_qualifier(CDS, "note")
            # get_start(CDS)
            # get_end(CDS)
            # get_strand(CDS)
