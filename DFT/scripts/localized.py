#!/usr/bin/env python
# Written by Joseph P.Vera
# 2024-10

"Code to extract information from EIGENVAL and PROCAR file to identify localized defects"
"The HOMO-LUMO transition refers to the transition between the Highest Occupied Molecular Orbital (HOMO) and the Lowest Unoccupied Molecular Orbital (LUMO)"
"When ----> Band number(s) = 0 : display the information in EIGENVAL file \
      ----> Band number(s) = 1, 2, ... , band : display and save information"

import os

archivo_eigenval = 'EIGENVAL'
file_path = 'PROCAR'

user_input = input('Band number(s): ') # example: 430,431,432 or 0 for EIGENVAL only
band_numbers = [int(band.strip()) for band in user_input.split(',')] 

# Extract folder name from current directory
folder_name = os.path.basename(os.getcwd())

# list to store the lines of the EIGENVAL file
lineas = []

# Read the EIGENVAL file and store the lines in a list
with open(archivo_eigenval, 'r') as f:
    lineas = f.readlines()

# variables to store the transition index
indice_transicion = None

# Loop through the lines to search for the transition
for i in range(len(lineas) - 1):
    # Separate the elements of the current line
    elementos_actual = lineas[i].split()
    elementos_siguiente = lineas[i + 1].split()
    
    # current line has at least 5 elements?
    if len(elementos_actual) >= 5 and len(elementos_siguiente) >= 5:
        # Check for the transition from 1 to another value in the fifth column
        if elementos_actual[4] == '1.000000' and elementos_siguiente[4] != '1.000000':
            indice_transicion = i + 1  
            break

# results for EIGENVAL output
eigenval_results = []

# Print the lines around the transition
if indice_transicion is not None:
    inicio = max(0, indice_transicion - 5)          # Lines above the transition
    fin = min(len(lineas), indice_transicion + 6)   # Lines below the transition
    eigenval_results.append(f"Defect: {folder_name}\n\n")
    eigenval_results.append("EIGENVAL:")
    eigenval_results.append("HOMO-LUMO transition\n")
    eigenval_results.append("Band     Energy(up)  Energy(down)   Occ(up)    Occ(down)")
    for j in range(inicio, fin):
        eigenval_results.append(lineas[j].strip())  # Append line without whitespace
else:
    eigenval_results.append("No transition found.")
    

# Function to parse PROCAR file for specified band in all blocks
def parse_procar_all_info(file_path, band_number):
    results = []
    current_block = []  # To store the current block's lines
    block_found = False

    with open(file_path, 'r') as file:
        for line in file:
            # Check for the start of a new block
            if line.strip().startswith("# of k-points"):
                if current_block:  # If we have a previous block stored, process it
                    block_found = False
                    for block_line in current_block:
                        if block_line.strip().startswith(f"band   {band_number}"):
                            block_found = True
                            results.append(f"\n\n###########################################")
                            results.append(f"PROCAR:")
                            results.append(f"Band {band_number}: Spin up")
                            results.append(f"{'ion':<8} {'s':<8} {'p':<8} {'d':<8} {'tot':<8}")
                            continue  
                        elif block_found:
                            if block_line.strip().startswith("ion"):
                                continue         # Skip the header line for ion columns
                            elif block_line.strip() == "":
                                continue         # Skip empty lines
                            elif "tot" in block_line:
                                break           

                            # Extract ion data
                            ion_data = block_line.split()
                            if len(ion_data) == 5:  # Expecting [ion, s, p, d, tot]
                                tot_value = float(ion_data[4])
                                # Only add to results if 'tot' > 0.1
                                if tot_value > 0.1:
                                    # Format the line to align the values
                                    formatted_line = f"{ion_data[0]:<8} {ion_data[1]:<8} {ion_data[2]:<8} {ion_data[3]:<8} {ion_data[4]:<8}"
                                    results.append(formatted_line)  # Only add the line if it's relevant

                current_block = []  # Reset current block for the next section

            # Store lines in the current block
            current_block.append(line)

        # Process the last block after the loop
        if current_block:
            block_found = False
            for block_line in current_block:
                if block_line.strip().startswith(f"band   {band_number}"):
                    block_found = True
                    results.append(f"\nBand {band_number}: Spin down")
                    results.append(f"{'ion':<8} {'s':<8} {'p':<8} {'d':<8} {'tot':<8}")
                    continue  
                elif block_found:
                    if block_line.strip().startswith("ion"):
                        continue      # Skip the header line for ion columns
                    elif block_line.strip() == "":
                        continue      # Skip empty lines
                    elif "tot" in block_line:
                        break         

                    # Extract ion data
                    ion_data = block_line.split()
                    if len(ion_data) == 5:  # Expecting [ion, s, p, d, tot]
                        tot_value = float(ion_data[4])
                        # Only add to results if 'tot' > 0.1
                        if tot_value > 0.1:
                            # Format the line to align the values
                            formatted_line = f"{ion_data[0]:<8} {ion_data[1]:<8} {ion_data[2]:<8} {ion_data[3]:<8} {ion_data[4]:<8}"
                            results.append(formatted_line)  # Only add the line if it's relevant

    return results

# list to hold all band information
all_band_info = []

# When user_input = 0, only display EIGENVAL information and exit
if band_numbers == [0]:
    for line in eigenval_results:
        print(line)
else:
    # Get band information for each specified band number
    for band_number in band_numbers:
        band_info = parse_procar_all_info(file_path, band_number)
        all_band_info.extend(band_info)  # Append results for the current band

    # Concatenate results
    final_results = eigenval_results + all_band_info

    # Create 'localized' folder if it doesn't exist
    localized_folder = '../localized/'
    if not os.path.exists(localized_folder):
        os.makedirs(localized_folder)

    # Save the results with folder name in the localized output folder
    output_file_path = os.path.join(localized_folder, f'localized_{folder_name}.dat')
    with open(output_file_path, 'w') as output_file:
        for line in final_results:
            output_file.write(line + '\n')

    #print("The file was saved")
    print("-------------------------------------------------------")
    print("-------------------------------------------------------")

    with open(output_file_path, 'r') as file:
    #    print("\nlocalized_defect.dat\n")
        for line in file:
            print(line.strip())
