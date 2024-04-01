#!/usr/bin/env python3

import argparse
import glob
import os
import cclib
from tabulate import tabulate
import csv

def has_imaginary_frequency(file_path):
    """
    Check if a Gaussian output file contains an imaginary frequency.

    Args:
        file_path (str): Path to the Gaussian output file.

    Returns:
        bool: State whether the logfile contains imaginary frequency or not.
    """
    hasZeroNegFreq = False
    
    try:
        data = cclib.io.ccread(file_path)
        frequencies = data.vibfreqs
        
        if any(freq < 0 for freq in frequencies):
            # The file contains an imaginary frequency."
            hasZeroNegFreq = False
        else:
            # The file does not contain an imaginary frequency.
            hasZeroNegFreq = True

    except Exception as e:
        print(f"""Error parsing file '{file_path}': {str(e)}
              Your frequency job might not be finished
              """)
        
    return hasZeroNegFreq


def has_optimized_geometry(file_path):
    """
    Check if a Gaussian output file contains an optimized geometry calculation.

    Args:
        file_path (str): Path to the Gaussian output file.

    Returns:
        bool: Has optimized geometry or not
    """
    isOptimized = False
    
    try:
        data = cclib.io.ccread(file_path)
        if hasattr(data, 'optstatus'):
            optstatus = data.optstatus
            if optstatus[-1] in [1, 5]:
                # Optimized Geometry is found
                isOptimized = True
            elif optstatus[-1] == 2:
                # Unoptimized geometry is found
                isOptimized = False
            else:
                # Unable to tell if is optimized or not, could be error related to memory
                isOptimized = False
        else:
            print(f"File '{file_path}' has no attribute optstatus.")

    except Exception as e:
        print(f"Error checking file '{file_path}': {str(e)}")

    return isOptimized

def export_to_csv(data, csvFilePath):
    if not data:
        print("Error: Data is empty. Nothing to export.")
        return
    
    try:
        with open(csvFilePath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        print(f"Data has been successfully exported to {csvFilePath}")

    except Exception as e:
        print(f"Error exporting data to CSV: {str(e)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check if Gaussian output file contains optimized geometry.')
    parser.add_argument('file_path', type=str, nargs='?', default='', help='Path to the Gaussian output file')
    parser.add_argument('-csv', action='store_true', help='Export data to CSV')

    args = parser.parse_args()

    if not args.file_path:
        args.file_path = os.path.join(os.getcwd(), '*.log')

    log_files = sorted(glob.glob(args.file_path))

    if log_files:
        table_data = []
        for log_file in log_files:
            optimized = has_optimized_geometry(log_file)
            frequency = has_imaginary_frequency(log_file)
            table_data.append([log_file, optimized, frequency])

        headers = ["Log File", "Is Optimized", "No Negative Frequency"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    else:
        print("No Gaussian output files found in the current directory.")

    if args.csv:
        csvFile = "optchk.csv"
        export_to_csv(table_data, csvFile)
    else:
        print("Data will not be exported to CSV.")