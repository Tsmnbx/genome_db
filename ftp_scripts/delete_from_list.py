### delete files fromt he list deletelist
import os
file = open("genome_db/deletelist","r")

while (1):
    file_name = file.readline().split()[1]
    print (file_name)
    os.remove(file_name)
