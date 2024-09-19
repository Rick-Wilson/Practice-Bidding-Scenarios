# Reads all .pbn files from directory /pbn and create command file for running BBA for each file
# generating a matching .pbn file for each .dlr

import os
import hashlib

def process_file(files):
    nfiles = 0
    for filename in files:
        if filename.lower().endswith('.pbn'):
            output_filename = filename.replace('.pbn', '.bba')
            if nfiles >3:
                break
            print("P:\\BBA.exe --ARCHIVE_FILE !P:\\bba\\" + output_filename + "! --AUTOBID --HAND !P:\\pbn\\" + filename + "! --CC1 GIB-ADB.bbsa -- CC2 GIB-ADB.bbsa --DD 0 --SD 1")
            nfiles += 1

def main():

    PBS_pbn = os.path.join(os.path.expanduser("~"), "Practice-Bidding-Scenarios/pbn/")

    current_directory_files = os.listdir(PBS_pbn)
    process_file(current_directory_files)

if __name__ == "__main__":
    main()
