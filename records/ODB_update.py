species_file = open('ODB_species_id.txt','r')
ids = species_file.readlines()

accession_file = open('3.accession_list','r')
accessions = accession_file.readlines()


outfile = open('ODB_Accession.txt','w')

for num in ids:
  #found = False
  for line in accessions:
    
    if num.strip() == line.split()[2]:
      outfile.write(line+'\n')
      #found = True
      
  #if not found:
  #  dne.append(num)
       
species_file.close()
accession_file.close()
   
