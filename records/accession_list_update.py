 
infile = open('3.accession_list','r') 
lines = infile.readlines()



outfile = open('3.accession_list_(z)','w')


for num in range(len(lines)):
  if num < 254:
    outfile.write(lines[num])
    continue
  
  
  outfile.write('\t'.join(str(num),lines[num].split()[1:]) + '\n')

infile.close()
outfile.close()