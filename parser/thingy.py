from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio.Alphabet import IUPAC

handle = open('abcd.gbff', 'rU')
for record in SeqIO.parse(handle, 'genbank'):
	print(record.name)
