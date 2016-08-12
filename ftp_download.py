import ftputil
from subprocess import call
import sys
import os

'''
USAGE: python ftp_download.py start_bacteria stop_bacteria [species_id_start] [file_id_start]
Output: A file named "summary" is updated with the list of species and bacteria that is downloaded and unzipped
start_id for species: check the last item in the summary

TODO:
- skip bacteria that doesnt have latest_assembly_versions folder DONE
- save the skipped bacteria list in a file
- skip bacteria that is already in the folder (or prompt if the user wants to download again)
- save the downloaded list in three files for db tables: summary, species list, file list
'''

def download():
    summary = open("summary",'a')

    startDIR = "/genomes/genbank/bacteria/"
    with ftputil.FTPHost("ftp.ncbi.nlm.nih.gov",'anonymous','') as ftp_host:
        ftp_host.chdir(startDIR)
        bacteria_list = ftp_host.listdir(ftp_host.curdir)

        print("Checking if the bacteria start and stop exists...")

        # Checking if start_bacteria exists in the database
        if (start_bacteria in bacteria_list):
            bacteria_start_id = bacteria_list.index(start_bacteria)
        else:
            print (start_bacteria + " not found in the list of bacteria")
            exit()

        # Checking if stop_bacteria exists in the database
        if (stop_bacteria in bacteria_list):
            bacteria_stop_id = bacteria_list.index(stop_bacteria)
        else:
            print (stop_bacteria + " not found in the list of bacteria")
            exit()

        # letting the user know which bacteria are being downloading
        print("Downloading the following bacteria...")
        for i in range(bacteria_start_id, bacteria_stop_id+1):
            print (str(i+1) + "\t" + bacteria_list[i])
        print ("total number of bacteria being downloaded: " + str(len(range(bacteria_start_id, bacteria_stop_id+1))))

        for i in range(bacteria_start_id, bacteria_stop_id+1):
            #loop through the bacteria being downloaded
            bacteria_name = bacteria_list[i]

            print ("\nSPECIES#" + str(i+1) + ": "+ bacteria_name)
            # ftp_host.chdir(bacteria_name+"/latest_assembly_versions")
            ftp_host.chdir(bacteria_name)

            if ("latest_assembly_versions" not in ftp_host.listdir(ftp_host.curdir)):
                print ("bacteria does not have a latest_assembly_versions folder: " + bacteria_name)

                ftp_host.chdir("../")
                continue

            assembly_list = ftp_host.listdir(ftp_host.curdir)
            ftp_host.chdir("../")

            # for assembly in assembly_list:
            #     ftp_host.chdir(assembly)
            #
            #     files = ftp_host.listdir(ftp_host.curdir)
            #     for file in files:
            #         if "_genomic.gbff.gz" in file:
            #             # downloaded to current director in terminal
            #             summary.write(str(file_count) + "\t" + str(species_count) + "\t" + bacteria_name + "\t" + file.strip(".gz") + "\n")
            #             print ("file#" + str(file_count) + ": " + file)
            #             ftp_host.download(file,file)
            #             print ("Unzipping")
            #             call(["gzip","-d",file])
            #             file_count+=1
            #
            #     ftp_host.chdir("../")
            #
            # ftp_host.chdir(startDIR)
            # species_count+=1
        print("done downloading")

def create_summary():
    path = os.path.normpath(os.path.join(os.getcwd(), "summary"))
    if os.path.exists(path.strip()):
        print("appending to existing summary file...")
    else:
        summary = open("summary",'w')
        summary.write("accession_key" + "\t" +  "species_id" + "\t" + "bacteria_name" + "\t" + "assembly_name" + "\n")


def check(): # checks which bacteria we can skip
  
  skipBac = open('skipBacteria.txt','a')
  startDIR = "./genomes/genbank/bacteria/"
  with ftputil.FTPHost("ftp.ncbi.nlm.nih.gov",'anonymous','') as ftp_host:
    ftp_host.chdir(startDIR)
    names = ftp_host.listdir(ftp_host.curdir)
    
    start = int(start_bacteria)
    count = start
    check_list = names[start:(start + 500) + 1 ]
    
   
    for name in check_list:
      ftp_host.chdir(name)
      if "latest_assembly_versions" not in ftp_host.listdir(ftp_host.curdir):
	#mark down bacteria w/o latest_assembly_versions 
	skipBac.write(str(count) + ')' + name + "\n")
	
	if count%50 == 0: 
	  print('.') # 1 dot / 50 bacteria
	  skipBac.write(str(count) + ')\n') # helps keep track
	  
      
      ftp_host.chdir("..")  # go back to list

      count += 1
    print('Checked upto (but excluding): ', count) # '''
      
'''
if (len(sys.argv) < 4):
    print("USAGE: python ftp_download.py species_start_id file_start_id bacteria_name_starts_with [bacteria_only_start_at]")
    exit()
'''

start_bacteria = sys.argv[1]
stop_bacteria = sys.argv[2]
species_count = int(sys.argv[3])
file_count = int(sys.argv[4]) # '''


# create_summary()
# download()
check()