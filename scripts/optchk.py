import argparse
import glob
import os
import cclib

def has_imaginary_frequency(file_path):
    """
    Check if a Gaussian output file contains an imaginary frequency.

    Args:
        file_path (str): Path to the Gaussian output file.

    Returns:
        str: State whether the logfile contains imaginary frequency or not.
    """
    try:
        data = cclib.io.ccread(file_path)
        frequencies = data.vibfreqs
        
        if any(freq < 0 for freq in frequencies):
            return print(f"The file '{log_file}' contains an imaginary frequency.")
        else:
            return print(f"The file '{log_file}' does not contain an imaginary frequency.")

    except Exception as e:
        print(f"""
              Error parsing file '{file_path}': {str(e)}
              Your frequency job might not be finished
              """)


def has_optimized_geometry(file_path):
    """
    Check if a Gaussian output file contains an optimized geometry calculation.

    Args:
        file_path (str): Path to the Gaussian output file.

    Returns:
        str: Statement whether the optimized geometry is found, unoptimized geometry is found, or failed to finish.
    """
    try:
        data = cclib.io.ccread(file_path)
        if hasattr(data, 'optstatus'):
            optstatus = data.optstatus
            if optstatus[-1] in [1, 5]:
                return print(f"Optimized geometry calculation found in file '{log_file}'.")
            elif optstatus[-1] == 2:
                return print(f"Unoptimized geometry calculation found in file '{log_file}'.")
            else:
                return print(f"Unable to tell if optimization completed or not '{log_file}'.")
        else:
            print(f"File '{log_file}' has no atribute optstatus.")

    except Exception as e:
        print(f"Error checking file '{file_path}': {str(e)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check if Gaussian output file contains optimized geometry.')
    parser.add_argument('file_path', type=str, nargs='?', default='', help='Path to the Gaussian output file')

    args = parser.parse_args()

    if not args.file_path:
        args.file_path = os.path.join(os.getcwd(), '*.log')

    log_files = sorted(glob.glob(args.file_path))

    if log_files:
        for log_file in log_files:
            has_optimized_geometry(log_file)

    if log_files:
        for log_file in log_files:
            has_imaginary_frequency(log_file)
    else:
        print("No Gaussian output files found in the current directory.")