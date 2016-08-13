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
    path = os.path.normpath(os.path.join(os.getcwd(), "summary"))
    if os.path.exists(path.strip()):
        print("Summary file found. New reports will be published on it...")
    else:
        print("creating new summary...")
        summary = open("summary",'w')

def create_species_list():
    path = os.path.normpath(os.path.join(os.getcwd(), "species_list"))
    if os.path.exists(path.strip()):
        print("appending to existing species list...")
    else:
        print("creating new species list...")
        species_file = open("species_list",'w')
        update_species_list (species_file, "species_key", "species_name")

def create_accession_list():
    path = os.path.normpath(os.path.join(os.getcwd(), "accession_list"))
    if os.path.exists(path.strip()):
        print("appending to existing accession file...")
    else:
        print("creating new accession file...")
        accession_file = open("accession_list",'w')
        update_accession_list (accession_file, "accession_key", "accession_name", "species_key")

def create_no_accession_list():
    path = os.path.normpath(os.path.join(os.getcwd(), "no_accession_list"))
    if os.path.exists(path.strip()):
        print("appending to existing no accession list file...")
    else:
        print("creating new no accession list file...")
        no_accession_file = open("no_accession_list",'w')
        no_accession_file.write("species_name")

def update_species_list(file, species_key, bacteria_name):
    file.write(str(species_key) + "\t" + bacteria_name + "\n")

def update_accession_list(file, accession_key, accession_name, species_key):
    file.write(str(accession_key) + "\t" + accession_name + "\t" + str(species_key) + "\n")

def download(bacteria_key, accession_key):
    # opening all the files that will be edited
    summary = open("summary", 'a')
    species_file = open("species_list", 'a')
    accession_file = open("accession_list", 'a')
    no_accession_file = open("no_accession_list", 'a')

    startDIR = "/genomes/genbank/bacteria/"

    with ftputil.FTPHost("ftp.ncbi.nlm.nih.gov",'anonymous','') as ftp_host:
        ftp_host.chdir(startDIR)
        bacteria_list = ftp_host.listdir(ftp_host.curdir)

        # bacteria_check function used to check if bacteria start and stop exists or not
        print("Checking if the bacteria start and stop exists...")
        bacteria_start_id = bacteria_check(bacteria_list, start_bacteria)
        bacteria_stop_id = bacteria_check(bacteria_list, stop_bacteria)

        # letting the user know which bacteria are being downloading
        print("Downloading the following bacteria...")
        for i in range(bacteria_start_id, bacteria_stop_id+1):
            print (bacteria_list[i])

        # updating summary
        summary.write (str(datetime.datetime.now()) + "\n")
        summary.write ("Downloaded: from " + start_bacteria + " to " + stop_bacteria + "\n")
        summary.write ("bacteria_key [start]: " + str(bacteria_key) + "\n")
        summary.write ("accession_key [start]" + str(accession_key) + "\n")

        for i in range(bacteria_start_id, bacteria_stop_id+1):
            #loop through the bacteria being downloaded
            bacteria_name = bacteria_list[i]
            update_species_list(species_file, bacteria_key, bacteria_name)

            print ("\nSPECIES#" + str(bacteria_key) + ": "+ bacteria_name)
            ftp_host.chdir(bacteria_name)

            if ("latest_assembly_versions" not in ftp_host.listdir(ftp_host.curdir)):
                print ("bacteria does not have a latest_assembly_versions folder: " + bacteria_name)
                no_accession_file.write(bacteria_name + "\n")
                ftp_host.chdir("../")
                break

            ftp_host.chdir("latest_assembly_versions")
            assembly_list = ftp_host.listdir(ftp_host.curdir)

            for assembly in assembly_list:
                # accessing every assembly folder in the species folder
                ftp_host.chdir(assembly)

                files = ftp_host.listdir(ftp_host.curdir)
                for file in files:
                    if "_genomic.gbff.gz" in file:
                        update_accession_list(accession_file, accession_key, file.strip(".gz"), bacteria_key)

                        # stdout information about which file (strain) is being downloaded right now
                        print ("file#" + str(accession_key) + ": " + file)
                        # downloading the file
                        ftp_host.download(file,file)

                        # unzipping the file that is downloaded
                        print ("Unzipping")
                        call(["gzip","-d",file])
                        accession_key+=1

                # moving back to the folder with all the assemblies
                ftp_host.chdir("../")

            # moving back to startDIR because all the assembly folders are symlinks
            ftp_host.chdir(startDIR)
            bacteria_key += 1

        # updating summary
        summary.write ("bacteria_key [stop]: " + str(bacteria_key-1) + "\n")
        summary.write ("accession_key [stop]: " + str(accession_key-1) + "\n")
        summary.write ("------------------------------------------------\n")

        print("done downloading")

'''
def check():# this is used to show there're bacteria w/ +1 latest versions
  vers_to_amt = {}
  startDIR = "./genomes/genbank/bacteria/"
  with ftputil.FTPHost("ftp.ncbi.nlm.nih.gov",'anonymous','') as ftp_host:
    ftp_host.chdir(startDIR)
    names = ftp_host.listdir(ftp_host.curdir)

    for name in names:
    ftp_host.chdir(name+"/latest_assembly_versions")

    names = ftp_host.listdir(ftp_host.curdir)

    amt = len(names)
    if amt in vers_to_amt:
      vers_to_amt[amt] += 1
    else:
      vers_to_amt[amt] = 1

    ftp_host.chdir("../..")  # go back to list

  for amt in vers_to_amt.keys():
    print("{}:  {}".format(amt,vers_to_amt[amt])) # amt of vers : count
'''

if (len(sys.argv) == 5):
    start_bacteria = sys.argv[1]
    stop_bacteria = sys.argv[2]
    bacteria_key = int(sys.argv[3])
    accession_key = int(sys.argv[4])

    create_summary()
    create_species_list()
    create_accession_list()
    download(bacteria_key, accession_key)

elif (len(sys.argv) < 5):
    print("USAGE: python ftp_download.py  start_bacteria  stop_bacteria  species_id_start  accession_id_start")
    exit()
