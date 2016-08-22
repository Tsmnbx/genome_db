records = open('ODB_species_p1.txt','r')

lines = records.readlines()
# print(lines)

unique_bacteria =  set()
for line in lines:
  items = line.split()
  
  if "#" in items[0]: # skip comments
    continue
  
  unique_bacteria.add("_".join(items[1:4]))

records.close()

id_list = open('2.species_list','r')

lines = id_list.readlines()

dne = []

for bacteria in unique_bacteria:
  found = False
  for l in lines:
    line = l.split()
    #print(line)
    if (line[1] in bacteria) or (bacteria in line[1]):
      print('{})\t{}'.format(line[0],line[1]))
      found = True
  
  if not found:
    dne.append(bacteria)
  
id_list.close()

for i in dne:
  print(i)