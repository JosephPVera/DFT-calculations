#!/usr/bin/env python
# Written by Joseph P.Vera
# 2024-10

"Code to extract information from EIGENVAL and PROCAR file to identify localized defects"

archivo_eigenval = 'EIGENVAL'
file_path = 'PROCAR'  

# Prompt the user to enter band numbers, separated by commas
user_input = input('Band number(s)(example: 430,431,432): ')
band_numbers = [int(band.strip()) for band in user_input.split(',')]  

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
    eigenval_results.append("EIGENVAL: HOMO-LUMO transition\n")
    for j in range(inicio, fin):
        eigenval_results.append(lineas[j].strip())  # Append line without whitespace
else:
    eigenval_results.append("No transition found.")

# Function to parse PROCAR file for specified band
def parse_procar_all_info(file_path, band_number):
    band_found = False
    results = []

    with open(file_path, 'r') as file:
        for line in file:
            # Check if the target band was found
            if line.strip().startswith(f"band   {band_number}"):
                band_found = True
                results.append(f"\nPROCAR: Band {band_number} ")
                # Add the column names to the results
                results.append(f"{'ion':<8} {'s':<8} {'p':<8} {'d':<8} {'tot':<8}")
                continue  
            
            if band_found:
                if line.strip().startswith("ion"):
                    continue                 # Skip the header line for ion columns
                elif line.strip() == "":
                    continue                 # Skip empty lines
                elif "tot" in line:
                    break                    
                    
                # Extract ion data
                ion_data = line.split()
                if len(ion_data) == 5:  # Expecting [ion, s, p, d, tot]
                    tot_value = float(ion_data[4])
                    # Only add to results if 'tot' > 0.1
                    if tot_value > 0.1:
                        # Format the line to align the values
                        formatted_line = f"{ion_data[0]:<8} {ion_data[1]:<8} {ion_data[2]:<8} {ion_data[3]:<8} {ion_data[4]:<8}"
                        results.append(formatted_line)  

    return results

# list to hold all band information
all_band_info = []

# Get band information for each specified band number
for band_number in band_numbers:
    band_info = parse_procar_all_info(file_path, band_number)
    all_band_info.extend(band_info)  # Append results for the current band

# Concatenate results
final_results = eigenval_results + all_band_info

# Save results
with open('localized_defect.dat', 'w') as output_file:
    for line in final_results:
        output_file.write(line + '\n')

print("The file was saved")