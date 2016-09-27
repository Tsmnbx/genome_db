from odb3parser import *

### change operon_start and operon_end if u wanna get some specific operons
### or get all of them, use:
### operon_start = 1
### operon_end = 5302

operon_start = 1
operon_end = 5302

with open("odb3.tsv",'r') as file:
    tsv = file.readlines()

    for id in range(operon_start,operon_end+1):

        operon = get_operon(tsv,id)

        ### getting all the attributes for the operon
        operon_koid = get_operon_koid(operon)
        operon_species = get_operon_species(operon)
        operon_subspecies = get_operon_subspecies(operon)
        operon_name = get_operon_name(operon)
        operon_genes = get_operon_genes(operon)
        operon_annotations = get_operon_annotation(operon)

        ### id returns the operon key for the table
        print (id)
        print (operon)
        print (operon_koid)
        print (operon_species)
        print (operon_subspecies)
        print (operon_name)
        print (operon_genes)
        print (operon_annotations)
