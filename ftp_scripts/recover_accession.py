import ftputil
from subprocess import call
import sys
import os
import datetime

'''
USAGE: python ftp_download.py start_bacteria stop_bacteria
Output: A file named "summary" is updated with the list of species and bacteria that is downloaded and unzipped
start_id for species: check the last item in the summary

TODO:
- skip bacteria that doesnt have latest_assembly_versions folder DONE
- save the skipped bacteria list in a file
- skip bacteria that is already in the folder (or prompt if the user wants to download again)
- save the downloaded list in three files for db tables: summary, species list, file list
'''

# Checks if a bacteria is in the bacteria_list from genbank
def bacteria_check(bacteria_list, bacteria):
    if (bacteria in bacteria_list):
        bacteria_id = bacteria_list.index(bacteria)
        return bacteria_id
    else:
        print (bacteria + " not found in the list of bacteria")
        exit()

# Functions for creating summary, and species and accession list

def create_summary():
    path = os.path.normpath(os.path.join(os.getcwd(), "1.summary"))
    if os.path.exists(path.strip()):
        print("Summary file found. New reports will be published on it...")
    else:
        print("creating new summary...")
        summary = open("1.summary",'w')

def create_species_list():
    path = os.path.normpath(os.path.join(os.getcwd(), "2.species_list"))
    if os.path.exists(path.strip()):
        print("appending to existing species list...")
    else:
        print("creating new species list...")
        species_file = open("2.species_list",'w')
        update_species_list (species_file, "species_key", "species_name")

def create_accession_list():
    path = os.path.normpath(os.path.join(os.getcwd(), "3.accession_list"))
    if os.path.exists(path.strip()):
        print("appending to existing accession file...")
    else:
        print("creating new accession file...")
        accession_file = open("3.accession_list",'w')
        update_accession_list (accession_file, "accession_key", "accession_name", "species_key")

def create_no_accession_list():
    path = os.path.normpath(os.path.join(os.getcwd(), "4.no_accession_list"))
    if os.path.exists(path.strip()):
        print("appending to existing no accession list file...")
    else:
        print("creating new no accession list file...")
        no_accession_file = open("4.no_accession_list",'w')
        no_accession_file.write("species_name")

def create_recovered_accession_list():
    path = os.path.normpath(os.path.join(os.getcwd(), "5.recovered_accession_list"))
    if os.path.exists(path.strip()):
        print("appending to existing accession file...")
    else:
        print("creating new accession file...")
        accession_file = open("5.recovered_accession_list",'w')
        update_accession_list (accession_file, "accession_key", "accession_name", "species_key")


def update_species_list(file, species_key, bacteria_name):
    file.write(str(species_key) + "\t" + bacteria_name + "\n")

def update_accession_list(file, accession_key, accession_name, species_key):
    file.write(str(accession_key) + "\t" + accession_name + "\t" + str(species_key) + "\n")

def recover():
    # opening all the files that will be edited
    accession_file = open("5.recovered_accession_list", 'a')
    species_file = open("2.species_list",'r')
    list_file = open("list", 'r')

    startDIR = "/genomes/genbank/bacteria/"
    accession_key = 1

    #reading in list as an array
    list_array_org = list_file.readlines()
    list_array = []
    for item in list_array_org:
        list_array.append(item.strip())

    #reading in list as an array for species list
    species_list_org = species_file.readlines()
    species_list = []
    for species in species_list_org:
        species_list.append(species.strip().split())

    with ftputil.FTPHost("ftp.ncbi.nlm.nih.gov",'anonymous','') as ftp_host:
        ftp_host.chdir(startDIR)
        bacteria_list = ftp_host.listdir(ftp_host.curdir)

        for bacteria_name in bacteria_list:
            for species in species_list:
                if (bacteria_name == species[1]):
                    #only enter bacteria if it is in our bacteria list
                    print ("\nSPECIES#" + str(species[0]) + ": "+ bacteria_name)
                    ftp_host.chdir(bacteria_name)

                    ftp_host.chdir("latest_assembly_versions")
                    assembly_list = ftp_host.listdir(ftp_host.curdir)

                    for assembly in assembly_list:
                        print (assembly)
                        if any(assembly in item for item in list_array):
                            print ("success")
                            update_accession_list(accession_file, accession_key, assembly, species[0])
                            accession_key += 1
                        else:
                            print ("last one reached for this bacteria")
                            break

                    # moving back to startDIR because all the assembly folders are symlinks
                    ftp_host.chdir(startDIR)

        print("done updating the accession numbers for the given bacteria")


create_recovered_accession_list()
recover()
