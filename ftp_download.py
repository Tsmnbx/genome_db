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
# def create_summary():
#     path = os.path.normpath(os.path.join(os.getcwd(), "summary"))
#     if os.path.exists(path.strip()):
#         print("appending to existing summary file...")
#     else:
#         summary = open("summary",'w')
#         summary.write("species_key" + "\t" + "bacteria_name" + "\t" + "accession_key" + "\t" + "accession_name\n")

def create_summary():
    path = os.path.normpath(os.path.join(os.getcwd(), "summary"))
    if os.path.exists(path.strip()):
        print("Summary file found. New reports will be published on it...")
    else:
        summary = open("summary",'w')
        close (summary)

def create_species_list():
    path = os.path.normpath(os.path.join(os.getcwd(), "species_list"))
    if os.path.exists(path.strip()):
        print("appending to existing species list...")
    else:
        species_file = open("species_list",'w')
        update_species_list (species_file, "species_key", "bacteria_name")
        close (species_file)

def create_accession_list():
    path = os.path.normpath(os.path.join(os.getcwd(), "accession_list"))
    if os.path.exists(path.strip()):
        print("appending to existing summary file...")
    else:
        accession_file = open("accession_list",'w')
        update_accession_list (accession_file, "accession_key", "accession_name", "species_key")
        close(accession_file)ta

def update_species_list(file, species_key, bacteria_name):
    file.write(species_key + "\t" + bacteria_name + "\n")

def update_accession_list(file, accession_key, accession_name, species_key):
    file.write(accession_key + "\t" + accession_name + "\t" + species_key + "\n)

def download():


def ftp_access():
    # opening all the files that will be edited
    summary = open("summary", 'a')
    species_file = open("species_list", 'a')
    accession_file = open("accession_list", 'a')

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
            print (str(i+1) + "\t" + bacteria_list[i])
        print ("total number of bacteria being downloaded: " + str(len(range(bacteria_start_id, bacteria_stop_id+1))))

        for i in range(bacteria_start_id, bacteria_stop_id+1):
            #loop through the bacteria being downloaded
            bacteria_id = i;
            bacteria_name = bacteria_list[i]

            print ("\nSPECIES#" + str(i+1) + ": "+ bacteria_name)
            ftp_host.chdir(bacteria_name)

            if ("latest_assembly_versions" not in ftp_host.listdir(ftp_host.curdir)):
                print ("bacteria does not have a latest_assembly_versions folder: " + bacteria_name)
                # writing null in summary for this species id
                summary.write(str(bacteria_id) + "\t" + bacteria_name + "\t" + str(file_count) + "\t" + file.strip(".gz") + "\n")
                species_file(str(bacteria_id) + "\t" + bacteria_name)
                ftp_host.chdir("../")
                continue

            assembly_list = ftp_host.listdir(ftp_host.curdir)
            print (assembly_list)

            for assembly in assembly_list:
                print (assembly)
                print (ftp_host.getcwd())
                # accessing every assembly folder in the species folder
                ftp_host.chdir(assembly)

                files = ftp_host.listdir(ftp_host.curdir)
                for file in files:
                    dowload()
                    if "_genomic.gbff.gz" in file:
                        summary.write(str(bacteria_id) + "\t" + bacteria_name + "\t" + str(file_count) + "\t" + file.strip(".gz") + "\n")
                        species_file(str(bacteria_id) + "\t" + bacteria_name)
                        accession_file.write(str(file_count) + "\t" + file.strip(".gz") + "\t" + str(bacteria_id))

                        # stdout information about which file (strain) is being downloaded right now
                        print ("file#" + str(file_count) + ": " + file)
                        ftp_host.download(file,file)

                        # unzipping the file that is downloaded
                        print ("Unzipping")
                        call(["gzip","-d",file])
                        file_count+=1

                # moving back to the folder with all the assemblies
                ftp_host.chdir("../")

            # moving back to startDIR because all the assembly folders are symlinks
            ftp_host.chdir(startDIR)

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

if (len(sys.argv) < 4):
    print("USAGE: python ftp_download.py start_bacteria stop_bacteria species_id_start start_accession_id_start")
    exit()

start_bacteria = sys.argv[1]
stop_bacteria = sys.argv[2]
file_count = int(sys.argv[3])

create_summary()
create_species_list()
create_accession_list()
ftp_access()
