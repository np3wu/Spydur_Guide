#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
gausswriter creates input files from user inputs.
For every element from H to Kr. The standard cc-pVTZ is employed
For any other element in row 5 or other, the smallest ECP and 
cc-pVTZ basis set is chosen. If pVTZ level is not accessible or 
non-existent, you can choose from a chosen set available
"""
# Credits
__author__ = 'Nam H. Pham'
__copyright__ = 'Copyright 2023'
__credits__ = None
__email__ = "nam.pham@richmond.edu"

# System imports
import os
import sys
import re
import gaussreader

# periodictable library
import periodictable
from periodictable import elements

# N-ary tree structures
from sloppytree import SloppyTree
from anytree import NodeMixin, RenderTree

# Data imports and exports
import json
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter

##################################################
#   Collects data for file template
##################################################

def collect_data() -> SloppyTree:
    """Collects data as a SloppyTree dictionary to parse into the template file.

    Returns:
        SloppyTree: sloppytree item containing all parsed items
    """
    data = SloppyTree()
    
    prompts = {
        'filename': 'Enter the name of the file (without extension): ',
        'mem': 'Enter the memmory: ',
        'nproc': 'Enter the number of processors: ',
        'input_line': 'Enter the input line: ',
        'job_title': 'Enter the job title: ',
        'charge': 'Enter the charge: ',
        'spin': 'Enter the spin: ',
        'geometry': 'Enter the geometry (paste multiple lines, press Ctrl+D when done):\n',
    }
    # Iterate over prompts and update data dictionary
    for key, value in prompts.items():
        
        if key == 'geometry':
            print(value, end='')
            geometry_lines = sys.stdin.readlines()
            geometry_input = ''.join(geometry_lines)
            data[key] = geometry_input        
        
        # Convert specific values to integers
        elif key in ['mem', 'nproc','charge', 'spin']:
            data[key] = int(input(value))
        
        else:
            data[key] = input(value)
        
    return data
    

def collect_data_from_existing(file: str) -> SloppyTree:
    data = gaussreader.gaussreader_main(file)
    
    prompts = {
        'filename': 'Enter the name of the file (without extension): ',
        'mem': 'Enter the memmory: ',
        'nproc': 'Enter the number of processors: ',        
        'job_title': 'Enter the job title: ',
        'charge': 'Enter the charge: ',
        'spin': 'Enter the spin: ',
        'geometry': 'Enter the geometry (paste multiple lines, press Ctrl+D when done):\n',
    }
    # Iterate over prompts and update data dictionary
    for key, value in prompts.items():
        
        if key == 'geometry':
            print(value, end='')
            geometry_lines = sys.stdin.readlines()
            geometry_input = ''.join(geometry_lines)
            data[key] = geometry_input        
        
        # Convert specific values to integers
        elif key in ['mem', 'nproc','charge', 'spin']:
            data[key] = int(input(value))
        
        else:
            data[key] = input(value)
        
    return data
    
def templatewriter():

    new_or_old = input("""
    Do you want to use an existing file in the folder as a template?
    This includes the memory, number of processors, and input line.
    If yes, include name of file (with extension) as template >>> """)
        
    negative_responses = ["n", "No", "no", "0", "", "\x1b"]
        
    if new_or_old.lower() not in negative_responses:
        current_dir = os.getcwd()
        template_file = os.path.join(current_dir,new_or_old)
        data = collect_data_from_existing(template_file)
        template = write_com_file(data)
    
    else:
        data = collect_data()
        template = write_com_file(data)
        
    return template, data
    
def write_com_file(data: SloppyTree):
    com_template = """%mem={}GB
%nproc={}
%chk= {}.chk
# {}
    
{}
    
{} {}
{}
"""
    #pretty up the geometry so that no syntax error occurs
    geometry = data['geometry']
    if geometry.endswith('\n'):
        data['geometry'] = geometry[:-1]    
    
    formatted_string = com_template.format(data.get('mem', ''),
                                            data.get('nproc', ''),
                                            data.get('filename', ''),
                                            data.get('input_line', ''),
                                            data.get('job_title', ''),
                                            data.get('charge', ''),
                                            data.get('spin', ''),
                                            data.get('geometry', ''))
    return formatted_string

##################################################
#   Import pseudopotential data from separate file
#   Process pseudopotential data
##################################################

def import_data_json(filename):
    """
    This function imports data from a jason file as imported_data.
    """
    with open(filename, "r") as file:
        try:
            importer = JsonImporter()
            json_data = json.loads(file.read())
                
            # Import the JSON data
            imported_data = importer.import_(json_data)
            
        except Exception as e:
            print(f"Cannot import data from {file}: {e}")
        
    return imported_data


def ECP_key_sorting(key):
    """Logic to sort the ECP in order of most physically accurate to least
    physically accurate. In the case where it does not match the logic, it returns
    the biggest value possible so that it doesnot interfere with the execution of 
    the code.

    Args:
        key (str): The key of a dictionary

    Returns:
        tuple: a tuple to use in a min function to pickout the smallest value
    """
    try:
        match = re.match(r'ECP(\d+)([SM])([A-Z]{2})', key)
        n = int(match.group(1))
        X = match.group(2)
        Y = match.group(3)
        X_order = {'S': 2, 'M': 1}
        Y_order = {'HF': 3, 'WB': 2, 'DF': 1}
        return (n, Y_order[Y], X_order[X])
    except Exception as e:
        
        return (200,4,3)
        

def get_ECP_data(ECP_data,symbol):
    """Logic to pick out the best pseudopotential and basis sets.
    Not recommended for the faint of heart

    Args:
        ECP_data (): Data from using import_data_json

    Returns:
        dict: dictionary values to parse into gausswriter
    """
    
    for element in ECP_data.children:
        if element.name == symbol:
            ECP_dict = get_dict_items_from_Anynode(element.children)
            pseudo_key = min(ECP_dict, key=ECP_key_sorting)
            pseudo_value = ECP_dict[pseudo_key]
            #print(pseudo_key)
            for pseudo in element.children:
                if pseudo.name == pseudo_key:
                    basis_dict = get_dict_items_from_Anynode(pseudo.children)
                    
                    _VTZ_basis = next((basis for basis in basis_dict if "_VTZ" in basis), None)
                    
                    if _VTZ_basis is not None:
                        basis_set = basis_dict[_VTZ_basis]
                        
                        #print(_VTZ_basis) #Testing to see if variable is accessible
                        #print(basis_set)
                        break

                        
                    else:
                        print("The default cc_pVTZ is not available")
                        for basis in basis_dict:
                            print(basis)
                        basis = input("Please choose from these options:")
                        basis_set = basis_dict[basis]
                        
                        #print(basis) #Testing to see if variable is accessible

    return{f"{symbol}_ECP": pseudo_value, f"{symbol}_Basis_sets": basis_set}

    

def get_dict_items_from_Anynode(data):
    """This function creates a dictionary value for every name value pair
    created in AnyNode

    Args:
        data (tuple): children of your anytree data

    Returns:
        dict: dictionary values of name and value pair
    """
    name_value_dict = {node.name: node.value for node in data}
    
    return name_value_dict

def get_list_items_from_Anynode(data):
    """This function creates a list value for every name or value
    created in AnyNode

    Args:
        data (tuple): children of your anytree data

    Returns:
        tuple[list, list]: tuple value of name amd value list
    """
    name = [node.name for node in data]
    value = [node.value for node in data]
    return name, value

##################################################
#   Parse chemical formula
##################################################

def parse_chemical_formula(formula):
    """Takes in a string of a chemical formula and parse it for Elemental symbol
    and count of atoms.

    Args:
        formula (_str_): _Chemical Formula of choice_

    Returns:
        _dict_: _symbol as key and count as value_
    """
    element_counts = {}
    
    i = 0
    while i < len(formula):
        if formula[i].isupper():
            element = formula[i]
            i += 1
            while i < len(formula) and formula[i].islower():
                element += formula[i]
                i += 1
            count = ""
            while i < len(formula) and formula[i].isdigit():
                count += formula[i]
                i += 1
            count = int(count) if count else 1
            element_counts[element] = element_counts.get(element, 0) + count
        else:
            i += 1
    
    return element_counts

def gausswriter_main():

    template, tree = templatewriter()
    
    chemical_formula = input("Enter a chemical formula: ")
    element_counts = parse_chemical_formula(chemical_formula)
    
    # Sorting the Chemical elements in order
    element_symbols = [element.symbol for element in periodictable.elements]
    sorted_elements = sorted(element_counts.items(), key=lambda x: element_symbols.index(x[0]))
    element_counts = dict(sorted_elements)
    
    no_pseudo_elements = [element for element in element_counts if element in element_symbols[:37]]
    pseudo_elements = [element for element in element_counts if element in element_symbols[37:]]

    for element in no_pseudo_elements:
        template += f"\n{element} 0"
        template += "\ncc-pVTZ"
        template += "\n****"

    
    # Json file housed all the pseudopotential scraped from the website
    # https://www.tc.uni-koeln.de/PP/clickpse.en.html
    # I have not figured out how to tie the data to the script so this is a temporary solution.
    json_file = "../gausswriter/tree_data_gaussian.json"
    ECP_data = import_data_json(json_file)

    if len(pseudo_elements) > 0:
        
        for symbol in pseudo_elements:
            data = get_ECP_data(ECP_data, symbol)
            # data includes 2 dictionary terms for pseudopotentials and basis sets
            template += "\n"
            template += data[f'{symbol}_Basis_sets']
            template += "\n****"

        i = 0
        while i < 2:
            template += "\n"
            i += 1    

        for symbol in pseudo_elements:
            data = get_ECP_data(ECP_data, symbol)
            template += data[f'{symbol}_ECP']
            template += "\n"
    else:
        print("No Pseudopotentials used for any element")

    if template.endswith('\n****'):
        template = template[:-4] 
    
    template += "\n\n\n \n"        
    folder_path = os.getcwd()
    
    file_path = os.path.join(folder_path, f"{tree['filename']}.com")
    
    with open(file_path, "w") as input_file:
        input_file.write(template)
        print(f"{input_file.name} has been generated")
            

##################################################
#   Execution
##################################################

if __name__ == '__main__':
    gausswriter_main()