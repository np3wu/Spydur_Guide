#!/usr/bin/env python3

import os

# Step 1: Create an empty list called "check_point_file_names"
check_point_file_names = []

# Step 2: Look through all the files in the folder. If the file ends in ".chk", add it to the list
folder_path = os.getcwd()  # Get the current working directory

for file_name in os.listdir(folder_path):
    if file_name.endswith(".chk"):
        check_point_file_names.append(file_name)

# Step 3: Run the python command on terminal inputting "formchk {check_point_file_names}"
for file_name in check_point_file_names:
    command = f"formchk {file_name}"
    os.system(command)