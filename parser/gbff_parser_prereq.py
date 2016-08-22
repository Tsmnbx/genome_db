from Bio import SeqIO
handle = open("abcd.gbff", "rU")
for record in SeqIO.parse(handle, "genbank"):
    print(record.subclasshook)
    #for thing in record.features[2]:
