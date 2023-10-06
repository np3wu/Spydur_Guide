import re
import pandas as pd
import numpy as np
import glob
import os

###########################################################
# Initiate capture functions
###########################################################

def nbo_start (file_path: str) -> list:
    start = 0
    begin = 0
    end = 0
    capture = []
    with open (file_path, 'r') as f:
        for line in f:
            # condition to end parsing
            if begin == 1 and ' NHO Directionality and "Bond Bending" (deviations from line of nuclear centers)' in line:
                end = 1
            # parse the chunk
            if start == 1 and begin == 1 and end == 0:
                if re.match(r"\s$", line): continue # if there's a space in the line
                capture += [line.rstrip('\n')]

            # First condition to initiate capture
            if ' NATURAL BOND ORBITAL ANALYSIS:' in line:
                print("Found condition for NBO data")
                start = 1

            if ' NATURAL BOND ORBITAL ANALYSIS, alpha spin orbitals:' in line:
                print("Found condition for NBO data for alpha spin orbital")
                start = 1            

            if ' NATURAL BOND ORBITAL ANALYSIS, beta spin orbitals:' in line:
                print("Found condition for NBO data for beta spin orbital")
                start = 1

            # Second condition to initiate capture    
            if start == 1 and '       (Occupancy)   Bond orbital/ Coefficients/ Hybrids' in line:
                begin = 1

    return capture

def nbo_summary_start (file_path: str) -> list:
    start = 0
    begin = 0
    end = 0
    capture = []
    with open (file_path, 'r') as f:
        for line in f:
            # Condition to end parsing
            if begin == 1 and '       -------------------------------' in line:
                end = 1
            # parse the chunk
            if start == 1 and begin == 1 and end == 0:
                if re.match(r"\s$", line): continue
                capture += [line.rstrip('\n')]

            # First condition to initiate capture
            if ' Natural Bond Orbitals (Summary):' in line:
                print("Found condition for NBO data")
                start = 1
            
            # Second condition to initiate capture    
            if start == 1 and '           NBO                        Occupancy    Energy   (geminal,vicinal,remote)' in line:
                begin = 1

    return capture


###########################################################
# Extraction script functions
###########################################################

def nbo_extract(lines: list, nbo_log_file: str) -> dict:

    nbo_log_file_name = os.path.splitext(os.path.basename(nbo_log_file))[0]

    filename = []
    orbnum= []
    occupancy = []
    bond_type = []
    index_orbital = []
    bonding_atom1 = []
    bonding_atom1_index = []
    bonding_atom2 = []
    bonding_atom2_index = []

    orbital_overlap = []
    coefficient = []
    coefficient_atom = []
    coefficient_atom_index = []

    s_contribution = []
    p_contribution = []
    d_contribution = []
    f_contribution = []
    g_contribution = []

    data = {
        'filename': filename, 'orbnum': orbnum, 'occupancy': occupancy, 'bond_type': bond_type, 'index_orbital': index_orbital,
        'bonding_atom1': bonding_atom1, 'bonding_atom1_index': bonding_atom1_index, 'bonding_atom2': bonding_atom2,
        'bonding_atom2_index': bonding_atom2_index, 'orbital_overlap': orbital_overlap, 'coefficient': coefficient, 
        'coefficient_atom': coefficient_atom, 'coefficient_atom_index': coefficient_atom_index, 
        's_contribution': s_contribution, 'p_contribution': p_contribution, 'd_contribution': d_contribution, 
        'f_contribution': f_contribution, 'g_contribution': g_contribution
    }

    # Pattern 1 works for both bonding and anti bonding orbitals
    #      1. (1.92175) BD ( 1)Pt   1 - I   2  
    #

    #Pattern2 works for both bonding and antibonding orbitals, also handles negative coefficient
    #                ( 19.41%)   0.4406*Pt   1 s( 40.72%)p 1.25( 51.03%)d 0.16(  6.36%)
    #                ( 80.59%)   0.8977* I   2 s( 19.17%)p 4.19( 80.40%)d 0.02(  0.38%)
    #             ( 94.13%)   0.9702* F   3 s(  0.00%)p 1.00( 99.91%)d 0.00(  0.09%)
    #                (  8.48%)  -0.2912* F   3 s( 31.31%)p 2.19( 68.56%)d 0.00(  0.13%)

    # Pattern 3 deals with if f orbital and g orbital inconsistencies
    #                                                  f 0.07(  3.21%)g 0.00(  0.07%)
    #                                                  f 0.00(  0.00%)
    # Fixed syntax error where (?:) is a non capturing group
    #
    pattern1 = r"\s+([0-9]+)\.\s+\(([^)]*)\)\s+(BD.)\(([^)]*)\)(.[A-Za-z]+)\s+([0-9]+)\s+\-(.[A-Za-z]+)\s+([0-9]+).+"    
    pattern2 = r"\s+\(([^)]*)\)\s+(.[0-9]*\.[0-9]+)\*(.[A-Za-z]+)\s+([0-9]+).s\(([^)]*)\)p(.[0-9]*\.[0-9]+)\(([^)]*)\)d(.[0-9]*\.[0-9]+)\(([^)]*)\)"
    pattern3 = r"\s+f(.[0-9]*\.[0-9]+)\(([^)]*)\)(g(.[0-9]*\.[0-9]+)\(([^)]*)\))?"

    #pattern 4 deals with non bonding lines. Currently not in use in the script, 
    #     5. (1.99956) CR ( 1)Pt   1           s(100.00%)p 0.00(  0.00%)d 0.00(  0.00%)
    #     6. (1.99934) CR ( 2)Pt   1           s(  0.00%)p 1.00(100.00%)
    #    18. (1.99998) CR ( 1) F   3           s(100.00%)
    #    19. (1.99968) LP ( 1)Pt   1           s(  0.00%)p 0.00(  0.00%)d 1.00( 99.98%)
    #    35. (0.00005) RY*( 8)Pt   1           s( 42.06%)p 0.61( 25.76%)d 0.67( 28.27%)
    #    36. (0.00000) RY*( 9)Pt   1           s(  0.00%)p 1.00( 99.94%)d 0.00(  0.00%)

    pattern4 = r"\s+([0-9]+)\.\s+\(([^)]*)\)\s+([A-Za-z]+.)\(([^)]*)\)(.[A-Za-z]+)\s+([0-9]+)\s+s\(([^)]*)\)(p\s+([0-9]*\.[0-9]+)\(([^)]*)\))?(d\s+([0-9]*\.[0-9]+)\(([^)]*)\))?"

    # index for logic system, 
    # i is for dealing with bonding orbitals where the lines printed is the combination 1 - 2 - 3 - 2 - 3
    # j is for dealing with non bonding orbitals where the lines can be pattern 4 - 4 or 4 - 3
    i = 0
    j = 0
    
    count = 0
    for line in lines:
        count += 1

        line1_match = re.match(pattern1, line)
        line2_match = re.match(pattern2, line)
        line3_match = re.match(pattern3, line)
        line4_match = re.match(pattern4, line)

        if line1_match and i == 0:
            i = 1
            for x in range(2):
                filename.append(nbo_log_file_name)
                orbnum.append(line1_match.group(1))
                occupancy.append(line1_match.group(2))
                bond_type.append(line1_match.group(3))
                index_orbital.append(line1_match.group(4))
                bonding_atom1.append(line1_match.group(5))
                bonding_atom1_index.append(line1_match.group(6))
                bonding_atom2.append(line1_match.group(7))
                bonding_atom2_index.append(line1_match.group(8))

        elif line2_match and i == 1:
            i = 2

            orbital_overlap.append(line2_match.group(1))
            coefficient.append(line2_match.group(2))
            coefficient_atom.append(line2_match.group(3))
            coefficient_atom_index.append(line2_match.group(4))
            s_contribution.append(line2_match.group(5))
            p_contribution.append(line2_match.group(7))
            d_contribution.append(line2_match.group(9))

        elif line3_match and i == 2:
            i = 3

            f_contribution.append(line3_match.group(2))
            g_contribution.append(line3_match.group(5))

        elif line2_match and i == 3:
            i = 4

            orbital_overlap.append(line2_match.group(1))
            coefficient.append(line2_match.group(2))
            coefficient_atom.append(line2_match.group(3))
            coefficient_atom_index.append(line2_match.group(4))
            s_contribution.append(line2_match.group(5))
            p_contribution.append(line2_match.group(7))
            d_contribution.append(line2_match.group(9))

        elif line3_match and i == 4:
            i = 0

            f_contribution.append(line3_match.group(2))
            g_contribution.append(line3_match.group(5))

        # if line4_match and j == 0:
        #     j = 1

        #     filename.append(nbo_log_file_name)
        #     orbnum.append(line4_match.group(1))
        #     occupancy.append(line4_match.group(2))
        #     bond_type.append(line4_match.group(3))
        #     bonding_atom1.append(line4_match.group(5))
        #     bonding_atom1_index.append(line4_match.group(6))
        #     bonding_atom2.append(None)
        #     bonding_atom2_index.append(None)

        #     orbital_overlap.append(None)
        #     coefficient.append(None)
        #     coefficient_atom.append(None)
        #     coefficient_atom_index.append(None)   

        #     s_contribution.append(line4_match.group(7))
        #     p_contribution.append(line4_match.group(9))
        #     d_contribution.append(line4_match.group(11))

        # elif line4_match and j == 1:
        #     j = 0

        #     filename.append(nbo_log_file_name)
        #     orbnum.append(line4_match.group(1))
        #     occupancy.append(line4_match.group(2))
        #     bond_type.append(line4_match.group(3))
        #     bonding_atom1.append(line4_match.group(5))
        #     bonding_atom1_index.append(line4_match.group(6))
        #     bonding_atom2.append(None)
        #     bonding_atom2_index.append(None)

        #     orbital_overlap.append(None)
        #     coefficient.append(None)
        #     coefficient_atom.append(None)
        #     coefficient_atom_index.append(None)            

        #     s_contribution.append(line4_match.group(7))
        #     p_contribution.append(line4_match.group(9))
        #     d_contribution.append(line4_match.group(11))
        #     f_contribution.append(None)
        #     g_contribution.append(None)

        # elif line3_match and j == 1:
        #     j = 0

        #     f_contribution.append(line3_match.group(2))
        #     g_contribution.append(line3_match.group(5))

        else:
            pass

    return data

def nbo_summary_extract(lines: list, nbo_log_file: str) -> dict:

    nbo_log_file_name = os.path.splitext(os.path.basename(nbo_log_file))[0]

    filename = []
    orbnum= []
    index_orbital = []
    occupancy = []
    bond_type = []
    bonding_atom1 = []
    bonding_atom1_index = []
    bonding_atom2 = []
    bonding_atom2_index = []
    energy = []

    data = {
        'filename': filename, 'orbnum': orbnum, 'bond_type': bond_type, 'index_orbital': index_orbital,
        'bonding_atom1': bonding_atom1, 'bonding_atom1_index': bonding_atom1_index,
        'bonding_atom2': bonding_atom2, 'bonding_atom2_index': bonding_atom2_index, 
        'occupancy': occupancy, 'energy': energy
    }

    # The pattern below deals with  the NBO summary data, i.e:
    #     1. BD (   1)Pt   1 - I   2          1.92175    -0.41262  156(g),154(g),32(g)
    #     2. BD (   2)Pt   1 - I   2          1.92057    -0.66994  157(g),129(v),28(g),132(v)
    #    151. RY*(  23) F   3                  0.00000     7.44235   
    #    157. BD*(   2)Pt   1 - F   3          0.08314     0.40079
    # This extracts relevent information in order: orbital number, bond type, atom 1, atom 2, atom index occupancy and energy in a.u   
    pattern = r"\s+([0-9]+)\.\s([A-Za-z]+\**)\s*\(([^)]*)\)\s?([A-Za-z]+)\s+([0-9]+)\s?-?\s?([A-Za-z]+)?\s\s\s([0-9]+)?\s+([0-9]*\.[0-9]+)\s+([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[Ee]([+-]?\d+))?"
    
    for line in lines:
        match = re.match(pattern, line)

        if match:
            filename.append(nbo_log_file_name)
            orbnum.append(match.group(1))
        
            bond_type.append(match.group(2))

            index_orbital.append(match.group(3))
            bonding_atom1.append(match.group(4))
            bonding_atom1_index.append(match.group(5))
            bonding_atom2.append(match.group(6))
            bonding_atom2_index.append(match.group(7))

            occupancy.append(match.group(8))
            energy.append(match.group(9))

    return data

###########################################################
# Data organization of storage
###########################################################

def replace_none_with_na (data: dict) -> dict:
    for key, values in data.items():
        for i, value in enumerate(values):
            if value is None:
                data[key][i] = '#N/A'

def tidy_data(data: dict) -> dict:
    tidied_data = {}

    for key, values in data.items():
        tidied_sublist = []

        for value in values:
            if value.endswith('%'):
                # Strip whitespace and remove '%' from string values
                stripped_value = value.strip().rstrip('%')
                try:
                    # Convert to float if it represents a percentage
                    converted_value = float(stripped_value) / 100
                except ValueError:
                    # If conversion to float fails, keep the original string value
                    converted_value = stripped_value

            elif type(value) is str:
                # Remove leading and trailing spaces from strings
                stripped_value = value.strip()
                # Try converting to interger
                try:
                    converted_value = float(stripped_value)
                    
                except ValueError:
                    # If conversion to float fails, keep the original string value
                    converted_value = stripped_value      
                          
            else:
                # Keep non-string values as-is
                converted_value = value

            tidied_sublist.append(converted_value)

        tidied_data[key] = tidied_sublist

    return tidied_data


def nbo_to_excel_main(file_paths: list[str], chosen_function_name):
    
    final_data = {}
    # #Create a list for the final and each file data
    dict_list = []  

    # Get the list of functions based on the chosen key (function group)
    chosen_function = function_mapping.get(chosen_function_name)
    if chosen_function:    

        for file_path in file_paths:
            print(f"Reading file:{file_path}")

            nbo_data_lines = chosen_function[0](file_path)
            data = chosen_function[1](nbo_data_lines, file_path)

            replace_none_with_na(data)
            data = tidy_data(data)

            dict_list.append(data)

    else:
        print("Invalid choice.")

    # Loop through the dictionaries
    for dictionary in dict_list:
        for key, values in dictionary.items():
            if key in final_data:
                final_data[key] += values  # Append values to existing key
            else:
                final_data[key] = values  # Add new key-value pair

    
    ###########################################
    # Testing if length is the same through out
    # lengths = set(len(sublist) for sublist in appended_list)
    # max_length = max(lengths)

    # for i, length in enumerate(lengths):
    #     if length < max_length:
    #         missing_value = i  # The missing value corresponds to the list index (1-indexed)
    #         print(f"List {missing_value} has a length of {length}, expected length is {max_length}.")

    # print(len(appended_list[16]))
    ##########################################

    df = pd.DataFrame(final_data)

    try:
        excel_name = input("\nEnter the name of the excel file without .xlsx: ")
        if excel_name == "":
            excel_name = "nbo_data"
        
        df.to_excel(f'{excel_name}.xlsx', sheet_name= 'nbo_data', index=False)
        print("Excel created successfully")
    except Exception as e:
        print(f"Something went wrong:{e}")
        

if __name__ == '__main__':
    folder_path = os.getcwd()  # Get the current working directory

    file_type = input('My NBO output files ends in: ')  # Specify the file type you want to search for (e.g., '*.txt')
    if file_type == '':
        file_type = '*.log'

    files = glob.glob(os.path.join(folder_path, file_type))  # Search for files in the current directory

    function_mapping = {
        'Extract Bonding NBOs': [nbo_start, nbo_extract],
        'Extract Summary NBO Section': [nbo_summary_start, nbo_summary_extract]
    }

    # Ask the user to choose a function
    print("Choose a function group to use:")
    for i, function_group in enumerate(function_mapping.keys(), 1):
        print(f"{i}. {function_group}")

    choice = input("Enter your choice (1-2): ")

    # Check if the choice is valid
    if choice in {'1', '2'}:
        chosen_function_name = list(function_mapping.keys())[int(choice) - 1]
        nbo_to_excel_main(files, chosen_function_name)
        
    else:
        print("Invalid choice.")
        chosen_function_name = None

        