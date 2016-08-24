 
infile = open('3.accession_list','r') 
lines = infile.readlines()



outfile = open('3.accession_list_(z)','w')


for num in range(len(lines)):
  if num < 254:
    outfile.write(lines[num])
    continue
  
  items = lines[num].split()
  outfile.write('\t'.join([str(num),items[1],items[2]]) + '\n')

infile.close()
outfile.close()