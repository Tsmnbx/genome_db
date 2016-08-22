from Bio import SeqIO
from parse_features import *

genome = list(SeqIO.parse("ecoli.gbff","genbank"))
locus = genome[0]

num_of_genes = len(locus.features)
local_gene_id = range(1, num_of_genes, 2)


#print (locus.features[4].qualifiers["gene"][0])
#print (locus.features[4].qualifiers["gene_synonym"])
#print (locus.features[4].qualifiers["function"][0].split(";"))
#print (locus.features[4].qualifiers["db_xref"])

CDS = locus.features[8]
source = locus.features[0]

print (get_sub_strain(source))
