infile = open('2.species_list','r') 
lines = infile.readlines()



outfile = open('2.species_list_(z)','w')


for num in range(len(lines)):
  if num < 8942:
    outfile.write(lines[num])
    continue
  
  outfile.write(str(num) + '\t' + lines[num].split()[1] + '\n')

infile.close()
outfile.close()