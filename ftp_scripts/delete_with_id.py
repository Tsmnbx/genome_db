### delete files according to the index numbers given in accession_list

import os
with open("3.accession_list") as fp:
    line = fp.readline().split()
    while (int(line[2]) < 12907):
        line = fp.readline().split()

    while (1):
        os.remove(line[1])
        line = fp.readline().split()

# os.chdir("..")
# print (os.getcwd())
# os.remove("dada")
