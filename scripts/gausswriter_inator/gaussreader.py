import sys
import os
import argparse
from sloppytree import SloppyTree
from fname import Fname
import linuxutils

NL = "\n"

def process_kv_lines(lines: list) -> dict:
    """
    Find the lines of input that contain "%k=v" type statements.
    Put the result in a dictionary, and return it.
    """
    data = {}

    for kv_line in (line.strip() for line in lines if line.startswith('%')):
        try:
            k, v = kv_line[1:].split('=')
            data[k] = v
        except Exception as e:
            print(f"Malformed line {kv_line=}")
            sys.exit(os.EX_DATAERR)

    return data

def process_resource_lines(lines: list) -> str:
    """
    Find any resource lines to be passed along to Gaussian.
    """
    resources = []

    for r_line in (line.strip()[1:] for line in lines if line.startswith('#')):
        resources.append(r_line.strip())

    return resources


def qg16_config(files: tuple) -> dict:
    """
    Process the files to build a dict of values and return it.
    """
    kv_dict = SloppyTree()
    lines = ""

    # Read all the files in the order in which they appear.
    # Add a NL in case the files are empty (or do not exist).
    for file_name in files:
        lines += Fname(file_name)() + NL

    # Create a list of lines, dropping any that are blank.
    lines = [_ for _ in lines.split(NL) if _]
    kv_dict = process_kv_lines(lines)
    kv_dict['input_line'] = NL.join(''.join(str(value) for value in values) for values in process_resource_lines(lines))

    return kv_dict

def gaussreader_main(file_name):
    """
    The primary function to build the SLURM job.
    """
    data = SloppyTree()

    # These may overwrite some of the default values.
    if (new_data := qg16_config((file_name,))):
        for k, v in new_data.items():
            data[k] = v

    # A little touch up for the units.
    data.mem = linuxutils.byte_size(data.mem)
    data.maxdisk = linuxutils.byte_size(data.maxdisk)
    data.minmem = linuxutils.byte_size(data.minmem)

    return data

if __name__ == '__main__':
    file_name = input("Gaussian filename to read (with extension)>>> ")
    
    f = Fname(file_name)
    if not f:
        sys.stderr.write(f"{str(f)} does not exist or you cannot read it.\n")
        sys.exit(os.EX_NOINPUT)
    file_name = str(f)

    try:
        vm_callable = "{}_main".format(os.path.basename(__file__)[:-3])
        sys.exit(globals()[vm_callable](file_name))
    except Exception as e:
        print(f"Unhandled exception {e}")
