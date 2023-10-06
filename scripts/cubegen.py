#!/usr/bin/env python3

import os
import subprocess

# Check the current folder location
current_folder = os.getcwd()
print("Current folder location:", current_folder)

# Find all file names that end with ".fchk"
fchk_files = [filename for filename in os.listdir(current_folder) if filename.endswith(".fchk")]

# Execute cubegen for each fchk_filename
for fchk_file in fchk_files:
    name_file_potential = fchk_file[:-5] + "_pot.cube"
    name_file_density = fchk_file[:-5] + "_den.cube"
    try:
        subprocess.run(
            f"cubegen 6 Potential=SCF {fchk_file} {name_file_potential} -3",
            shell=True,
            check=True
        )
        print(f"First cubegen executed successfully for {fchk_file}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the first cubegen for {fchk_file}:")
        print(e)

    try:
        subprocess.run(
            f"cubegen 6 Density=SCF {fchk_file} {name_file_density} -3",
            shell=True,
            check=True
        )
        print(f"Second cubegen executed successfully for {fchk_file}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the second cubegen for {fchk_file}:")
        print(e)

print("Task completed successfully.")