 
infile = open('3.accession_list','r') 
lines = infile.readlines()



outfile = open('3.accession_list_(z)','w')


for num in range(len(lines)):
  if num < 254:
    outfile.write(lines[num])
    continue
  
  items = lines[num].split()
  
  int_id = int(items[2])
  if int_id > 8942:
    outfile.write('\t'.join([str(num),items[1],str(int_id-1)]) + '\n')
    continue
      
  outfile.write('\t'.join([str(num),items[1],items[2]]) + '\n')

infile.close()
outfile.close()