#!/usr/bin/env python3

import os
import time
import subprocess

# Step 1: Get the list of .chk file names
folderpath = os.getcwd()
print("Current folder location:", folderpath)

chk_files = [file for file in os.listdir(folderpath) if file.endswith('.chk')]
print("List of .chk files:", chk_files)

if len(chk_files) == 0:
    print("No .chk files found. Exiting the program.")
    exit()

# Step 2: Extract the file names without the ".chk" extension
file_names = [file[:-4] for file in chk_files]

# Step 3: Create a for loop to perform the actions
for file_name in file_names:
    # Step 3a: Ask the user for input
    user_input = input(f"Perform NBO calculation on {file_name}? yes(y)/no(n): ").lower()

    # Step 3b: Check user input and proceed accordingly
    if user_input in ['yes', 'y']:
        # Step 3c: Create the template
        template = '''%mem=10gb
%nproc=12
%chk={}.chk
# geom=allcheck pop=nboread guess=read genchk chkbasis

NBO analysis of {}

$nbo BNDIDX $end'''

        template = template.format(file_name, file_name)

        # Step 3d: Write out the template to "filename.com"
        with open(f"{file_name}_nbo.com", "w") as f:
            f.write(template)

        # Step 3e: Execute "sg16 nbo.com" using subprocess
        subprocess.run([f"qg16 {file_name}_nbo.com"], shell = True)

        # Step 3f: Wait for 2 seconds
        time.sleep(2)
    elif user_input in ['no', 'n']:
        print(f"Skipping NBO calculation for {file_name}.")
    else:
        print("Invalid input. Skipping NBO calculation.")
