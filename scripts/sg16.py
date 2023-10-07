#!/usr/bin/env python3

import os
import argparse
import subprocess

def create_slurm_file(jobname):
    slurm_template = """#!/bin/bash

#SBATCH --account=####  ## your username
#SBATCH --mail-user=####   ## your email address
#SBATCH --mail-type=BEGIN  ## slurm will email you when your job starts
#SBATCH --mail-type=END  ## slurm will email you when your job ends

#SBATCH --job-name={}  ## Name of the job
#SBATCH --ntasks=1  ## number of tasks (analyses) to run
#SBATCH --cpus-per-task=12  ## the number of threads allocated to each task
#SBATCH --mem=12GB   # memory per CPU core

#SBATCH --partition=basic  ## the partitions to run in (comma separated)
#SBATCH --time=0  ## time for analysis (day-hour:min:sec)

#SBATCH -o slurm-%j.out
# #SBATCH -e slurm-%j.err
echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"

## Load modules
module load gaussian/gaussian

## Insert code, and run your programs here (use 'srun').

# Get the directory path
directory=$PWD

# Change to the specified directory
cd $directory

# Run Gaussian command
g16 {}.com {}.log
""".format(jobname,jobname,jobname)

    # Create or open the .slurm file in edit mode
    with open(".slurm", "w") as slurm_file:
        slurm_file.write(slurm_template)

    print("Created the .slurm file.")

def main():
    # Check the directory path
    directory = os.getcwd()
    print("Current directory: ", directory)

    # Parse the jobname argument
    parser = argparse.ArgumentParser(
        prog="sg16",
        description="Create and send a Gaussian job to the SLURM manager on SPYDUR."
    )
    parser.add_argument('jobname', help="Name of the job. Usually ends with .com")
    args = parser.parse_args()
    jobname = args.jobname

    # Create or open the .slurm file
    create_slurm_file(jobname)

    # Send the job in the command line
    subprocess.run("sbatch .slurm", shell=True)

if __name__ == "__main__":
    main()
