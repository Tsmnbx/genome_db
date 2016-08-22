records = open('OBD_species_p1.txt','w')

lines = records.readlines()

unique_bacteria =  set()
for line in lines:
  items = line.split()
  
  if "#" in items[0]: # skip comments
    continue
  
  unique_bacteria.add(items[1])

for i in unique_bacteria:
  print(i)
  
records.close()