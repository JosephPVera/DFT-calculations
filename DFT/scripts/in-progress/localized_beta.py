#!/usr/bin/env python3
# Written by Joseph P.Vera
# 2024-10

"This code need to implement new ideas, but can plot band vs tot for check the localized states."
"IMPROVE: VBM, CBM and 1000 (in for j in range(max(0, i - 1000)). branches??? " 
"sum the first 5 values ​​closest to 1"
import xml.etree.ElementTree as ET
import os
import argparse
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

"Usage: ----> localized.py         # all information within the band gap (occupied, unoccupied, partially occupied), if they exist at all \
        ----> localized.py --occ   # only occupied sates within the the band gap, if they exist at all \
        ----> localized.py --nocc  # only unoccupied sates within the the band gap, if they exist at all \
        ----> localized.py --pocc  # only partially occupied sates within the the band gap, if they exist at all"
        
"Code use information from EIGENVAL and vasprun.xml"
"There are three sub codes:  \
       ----> The first code is a counter of superblock, blocks and subblocks in vasprun.xml. \
       ----> The second code parse the EIGENVAL file and sort the information about Spin up, kpoint (up), band (up), Spin down \
              kpoint (down) and band (down), only filters energy values (column 2 and 3) between VBM and CBM following the break of 1.000 \
              in the column 4 and 5 (when continuity of 1.00 is broken)(HOMO-LUMO transition). That information is store in lists as band_index_list_up, \
              kpoint_list_up, spin_list_up, band_index_list_down, kpoint_list_down and spin_list_down. \
       ----> The third code use the band_index_list_up, kpoint_list_up, spin_list_up, band_index_list_down, kpoint_list_down and spin_list_down lists \
              and parse each value of the list for get the desired information."
    

input_file_path = 'EIGENVAL'  
output_file_path = 'eigenval_infos.dat' 

tree = ET.parse('vasprun.xml')
root = tree.getroot()



"Counters"
"Superblock (Spin), block (kpoint) and subblock (band) counters"
# Key words: ---->  superblock Spin up: <set comment="spin1">
#            ---->  superblock Spin down: <set comment="spin2">
#            ---->  block kpoint N: <set comment="kpoint 1">
#            ---->  subblock band N: <set comment="band 1">
superblock_count = 0
block_count = 0
subblock_count = 0

# Search for superblocks (spin1 and spin2)
for spin_set in root.findall(".//set[@comment='spin1']") + root.findall(".//set[@comment='spin2']"):
    superblock_count += 1
    
    # Search for blocks (kpoints) within each superblock
    for kpoint in spin_set.findall(".//set"):
        if 'kpoint' in kpoint.get('comment', ''):
            block_count += 1
            
            # Search for subblocks (bands) within each block
            for band in kpoint.findall(".//set"):
                if 'band' in band.get('comment', ''):
                    subblock_count += 1

# Print the results
print(f'Superblocks (Spin up and Spin down): {superblock_count}')
print(f'Blocks (kpoints) per superblock: {block_count / 2:.0f}')
print(f'Subblocks (bands) per superblock: {subblock_count / 2:.0f}')
print("##########################################################################################")




"Parsing the EIGENVAL file"
# Parse commands arguments for filter options
parser = argparse.ArgumentParser(description="Parse EIGENVAL and vasprun.xml files with optional filtering by occupancy label.")
parser.add_argument('--occ', action='store_true', help="Save only Occupied values")
parser.add_argument('--nocc', action='store_true', help="Save only Unoccupied values")
parser.add_argument('--pocc', action='store_true', help="Save only Partially Occupied values")
args = parser.parse_args()

# Define filtering options based on arguments
filter_occupancy = []
if args.occ:
    filter_occupancy.append("Occupied")
if args.nocc:
    filter_occupancy.append("Unoccupied")
if args.pocc:
    filter_occupancy.append("Partially Occupied")

# Lists to store Spin up, kpoint (up), band (up), Spin down, kpoint (down), band (down), energies (up), and energies (down)
band_index_list_up = []
kpoint_list_up = []
spin_list_up = []
energies_spin_up_list = []  # List to store energies for spin up

band_index_list_down = []
kpoint_list_down = []
spin_list_down = []
energies_spin_down_list = []  # List to store energies for spin down

# VBM and CBM 
VBM = -25 #7.2945 
CBM = 25 #11.7449 

# Read the file and store the blocks
with open(input_file_path, 'r') as file:
    # Skip the first 5 lines
    for _ in range(5):
        next(file) 

    # Read line 6 to get the block size, third value
    block_info = next(file).strip()
    if block_info:
        values = block_info.split()
        if len(values) >= 3:
            block_length = int(values[2]) + 1  # Block length + 1 for the extra blank line
        else:
            raise ValueError("Line 6 does not have enough values.")

    # Skip line 7 (blank line)        
    next(file)
    
    # Read the rest of the file
    lines = file.readlines()

blocks = [lines[i:i + block_length] for i in range(0, len(lines), block_length + 1)]  # +1 for blank lines
        
# Function to analyze each block 
def analyze_block(block, block_num, output_file):
    output_file.write("###########################################################\n")
    output_file.write(f"                          kpoint {block_num}                   \n")
    output_file.write("###########################################################\n")
    output_file.write(block[0].strip() + "\n")  # Write the first line (k-point coordinates) of each block
    
    # Ignore the first line (k-point coordinates) and process the following lines in the block
    data = [line.split() for line in block[1:]]
    
    # Convert columns 1, 2, 3, 4, and 5 to lists of numbers
    band_indices = [int(row[0]) for row in data]
    energies_spin_up = [float(row[1]) for row in data]
    occupancies_spin_up = [float(row[3]) for row in data]
    energies_spin_down = [float(row[2]) for row in data]
    occupancies_spin_down = [float(row[4]) for row in data]

    # Look for the break point in spin up occupancy
    for i, occ in enumerate(occupancies_spin_up):
        if occ != 1.0: 
            output_file.write("\nBand(up)   Energy(up)     Occ(up)    Occupancy\n")
            for j in range(max(0, i - 1000), min(len(band_indices), i + 1000)): # above the break of 1.000 and below the break of 1.000 #####################################
                if VBM < energies_spin_up[j] < CBM: # Compare the column 2 with VBM and CBM
                    label = (
                        "Occupied" if occupancies_spin_up[j] > 0.9 else
                        "Unoccupied" if occupancies_spin_up[j] < 0.1 else
                        "Partially Occupied"
                    )
                    if not filter_occupancy or label in filter_occupancy:
                        # Store band index, k-point, and spin for spin up
                        band_index_list_up.append(band_indices[j])
                        kpoint_list_up.append(block_num)
                        spin_list_up.append(1) # 1 for spin up
                        energies_spin_up_list.append(energies_spin_up[j])  # Store energy for spin up
                        output_file.write(f"{band_indices[j]:<10} {energies_spin_up[j]:<14.6f} {occupancies_spin_up[j]:<10.6f} {label}\n")
            break

    # Look for the break point in spin down occupancy
    for i, occ in enumerate(occupancies_spin_down):
        if occ != 1.0:
            output_file.write("\nBand(down) Energy(down)   Occ(down)  Occupancy\n")
            for j in range(max(0, i - 1000), min(len(band_indices), i + 1000)): # above the break of 1.000 and below the break of 1.000 ###################################
                if VBM < energies_spin_down[j] < CBM: # Compare the column 3 with VBM and CBM
                    label = (
                        "Occupied" if occupancies_spin_down[j] > 0.9 else
                        "Unoccupied" if occupancies_spin_down[j] < 0.1 else
                        "Partially Occupied"
                    )
                    if not filter_occupancy or label in filter_occupancy:
                        # Store band index, k-point, and spin for spin down
                        band_index_list_down.append(band_indices[j])
                        kpoint_list_down.append(block_num)
                        spin_list_down.append(2) # 2 for spin down
                        energies_spin_down_list.append(energies_spin_down[j])  # Store energy for spin down
                        output_file.write(f"{band_indices[j]:<10} {energies_spin_down[j]:<14.6f} {occupancies_spin_down[j]:<10.6f} {label}\n")
            break

# Analyze each block and save in eigenval_infos.dat file
with open(output_file_path, 'w') as output_file:
    for block_num, block in enumerate(blocks, start=1):
        analyze_block(block, block_num, output_file)

# Print the lists for spin up and spin down
print("Spin Up - Band index list:", band_index_list_up)
print("Spin Up - kpoint list:", kpoint_list_up)
print("Spin Up - Spin list:", spin_list_up)
print("Spin Up - Energies list:", energies_spin_up_list)  # Print the energies for spin up

print("Spin Down - Band index list:", band_index_list_down)
print("Spin Down - kpoint list:", kpoint_list_down)
print("Spin Down - Spin list:", spin_list_down)
print("Spin Down - Energies list:", energies_spin_down_list)  # Print the energies for spin down
print("##########################################################################################")
#print("The eigenval_infos.dat file has been saved.")







"Parsing the vasprun.xml file using the band_index_list_up, kpoint_list_up, spin_list_up, band_index_list_down, \
 kpoint_list_down lists and spin_list_down as inputs."
with open('vasprun_infos.dat', 'w') as file:
    # Prepare to store results
    results_up = []  # List to hold the band number and sum closest to one

    # Spin up analysis
    if band_index_list_up and kpoint_list_up and spin_list_up:
        file.write("########################################################################\n")
        file.write("                               SPIN UP                                  \n")
        file.write("########################################################################\n")

        for i in range(len(band_index_list_up)):
            # Assign values from the band_index_list_up, kpoint_list_up, spin_list_up lists
            spin_number = spin_list_up[i]        # input
            kpoint_number = kpoint_list_up[i]    # input
            band_number = band_index_list_up[i]  # input

            # Load the vasprun.xml file
            # tree = ET.parse('vasprun.xml')
            # root = tree.getroot()

            # Find the spin up (1) superblock
            spin_set = root.find(f".//set[@comment='spin{spin_number}']")

            if spin_set is not None:
                # file.write(f"Information of superblock 'spin{spin_number}':\n")
                
                # Find the block corresponding to the kpoint
                kpoint_block = spin_set.find(f".//set[@comment='kpoint {kpoint_number}']")
                
                if kpoint_block is not None:
                    file.write("########################################################################\n")
                    file.write(f"                               KPOINT {kpoint_number}                             \n")
                    file.write("########################################################################\n")
                    
                    # Find the subblock corresponding to the band
                    band_subblock = kpoint_block.find(f".//set[@comment='band {band_number}']")
                    
                    if band_subblock is not None:
                        file.write(f"Information of {band_subblock.attrib['comment']}:\n")
                        file.write(f"{'index':<6} {'s':<10} {'p':<10} {'d':<10} {'tot':<10}\n")
                        
                        # List to store total_sum values less than 1
                        less_than_one_up = []
                        
                        # Print the subblock information with filter
                        for j, child in enumerate(band_subblock):
                            columns = child.text.split()
                            total_sum = sum(float(value) for value in columns)
                            # keep the complete decimals from vasprun.xml
#                            formatted_sum = f"{total_sum:.{len(columns[0].split('.')[-1])}f}"
                            
                            # set the decimals
                            formatted_values = [f"{float(value):.3f}" for value in columns]
                            formatted_sum = f"{total_sum:.3f}"
                            
                            # Only print if "tot" is greater than 0.1
                            if float(formatted_sum) > 0.1:
                                # keep the decimals from vasprun.xml
#                                file.write(f"{j + 1:<6} {columns[0]:<10} {columns[1]:<10} {columns[2]:<10} {formatted_sum:<10}\n")
                                # set the decimals
                                file.write(f"{j + 1:<6} {formatted_values[0]:<10} {formatted_values[1]:<10} {formatted_values[2]:<10} {formatted_sum:<10}\n")

                            # Collect total_sum values less than 1
                            if total_sum < 1:
                                less_than_one_up.append(total_sum)

                        # Find the first 5 values closest to 1 (but less than 1)
                        first_five_closest_to_one = sorted(less_than_one_up, key=lambda x: 1 - x)[:5] ######################################################################
                        # Print values to console with four decimal places
#                        print(f"First 5 values closest to 1: {[f'{val:.4f}' for val in first_five_closest_to_one]}") ############################################## 
#
                        # Calculate and print the sum of the first 5 values closest to 1 
                        sum_closest_to_one = sum(first_five_closest_to_one)
#                        print(f"Sum of the first 5 values closest to 1: {sum_closest_to_one:.4f}") ##########################################################################

                        # Store band number and sum closest to one
                        energy = energies_spin_up_list[i]
                        results_up.append((band_number, sum_closest_to_one, energy))

                    else:
                        file.write(f"Subblock 'band {band_number}' not found in 'kpoint {kpoint_number}'.\n")
                else:
                    file.write(f"Block 'kpoint {kpoint_number}' not found in 'spin{spin_number}'.\n")
            else:
                file.write(f"Superblock 'spin{spin_number}' not found.\n")



    if band_index_list_down and kpoint_list_down and spin_list_down:
        file.write("\n\n\n")
        file.write("########################################################################\n")
        file.write("                               SPIN DOWN                                \n")
        file.write("########################################################################\n")

        results_down = []  # List to hold the band number and sum closest to one for spin down

        for i in range(len(band_index_list_down)):
            # Assign values from the band_index_list_down, kpoint_list_down, spin_list_down lists
            spin_number = spin_list_down[i]
            kpoint_number = kpoint_list_down[i]
            band_number = band_index_list_down[i]

            # Load the vasprun.xml file
            # tree = ET.parse('vasprun.xml')
            # root = tree.getroot()

            # Find the spin down (2) superblock
            spin_set = root.find(f".//set[@comment='spin{spin_number}']")

            if spin_set is not None:
                # file.write(f"Information of superblock 'spin{spin_number}':\n")
                
                # Find the block corresponding to the kpoint
                kpoint_block = spin_set.find(f".//set[@comment='kpoint {kpoint_number}']")
                
                if kpoint_block is not None:
                    file.write("########################################################################\n")
                    file.write(f"                               KPOINT {kpoint_number}                             \n")
                    file.write("########################################################################\n")
                    
                    # Find the subblock corresponding to the band
                    band_subblock = kpoint_block.find(f".//set[@comment='band {band_number}']")
                    
                    if band_subblock is not None:
                        file.write(f"Information of {band_subblock.attrib['comment']}:\n")
                        file.write(f"{'index':<6} {'s':<10} {'p':<10} {'d':<10} {'tot':<10}\n")
                        
                        # List to store total_sum values less than 1
                        less_than_one = []

                        # Print the subblock information with filter
                        for j, child in enumerate(band_subblock):
                            columns = child.text.split()
                            total_sum = sum(float(value) for value in columns)
                            # keep the complete decimals from vasprun.xml
#                            formatted_sum = f"{total_sum:.{len(columns[0].split('.')[-1])}f}"
                            
                            # set the decimals
                            formatted_values = [f"{float(value):.3f}" for value in columns]
                            formatted_sum = f"{total_sum:.3f}"
                            
                            # Only print if "tot" is greater than 0.1
                            if float(formatted_sum) > 0.1:
                                # keep the decimals from vasprun.xml
#                                file.write(f"{j + 1:<6} {columns[0]:<10} {columns[1]:<10} {columns[2]:<10} {formatted_sum:<10}\n")
                                # set the decimals
                                file.write(f"{j + 1:<6} {formatted_values[0]:<10} {formatted_values[1]:<10} {formatted_values[2]:<10} {formatted_sum:<10}\n")

                            # Collect total_sum values less than 1
                            if total_sum < 1:
                                less_than_one.append(total_sum)

                        # Find the first 5 values closest to 1 (but less than 1)
                        first_five_closest_to_one = sorted(less_than_one, key=lambda x: 1 - x)[:5] ##############################################################################
                        # Print values to console with four decimal places
#                        print(f"First 5 values closest to 1 (Spin Down): {[f'{val:.4f}' for val in first_five_closest_to_one]}")  ##############################################
#
                        # Calculate and print the sum of the first 5 values closest to 1
                        sum_closest_to_one = sum(first_five_closest_to_one)
#                        print(f"Sum of the first 5 values closest to 1 (Spin Down): {sum_closest_to_one:.4f}") ##################################################################

                        # Store band number and sum closest to one for spin down
                        energy = energies_spin_down_list[i]
                        results_down.append((band_number, sum_closest_to_one, energy))

                    else:
                        file.write(f"Subblock 'band {band_number}' not found in 'kpoint {kpoint_number}'.\n")
                else:
                    file.write(f"Block 'kpoint {kpoint_number}' not found in 'spin{spin_number}'.\n")
            else:
                file.write(f"Superblock 'spin{spin_number}' not found.\n")

#print("The vasprun_infos.dat file has been saved.")










def find_blocks(data):
    """
    Finds consecutive blocks in the first column of the list of tuples.
    Returns a list of blocks, where each block is a list of tuples.
    """
    blocks = []
    current_block = [data[0]]

    for i in range(1, len(data)):
        # If the difference between the current value and the previous one is not 1, consecutiveness breaks
        if data[i][0] == data[i - 1][0] + 1:
            current_block.append(data[i])
        else:
            blocks.append(current_block)
            current_block = [data[i]]
    
    # Add the last block
    if current_block:
        blocks.append(current_block)
    
    return blocks

def plot_blocks(results, title_prefix="", sigma=2):
    """
    Plots consecutive blocks of data and saves each plot in a file.
    """
    blocks = find_blocks(results)
    
    # Create a folder to save the plots if it doesn't exist
    output_folder = f"{title_prefix}_plots"
    os.makedirs(output_folder, exist_ok=True)
    
    for idx, block in enumerate(blocks):
        # Extract columns for each block
        band_numbers = [item[0] for item in block] 
        sum_closest_to_one = [item[1] for item in block]
        
        sum_smoothed = gaussian_filter1d(sum_closest_to_one, sigma=sigma)
        # Create the figure
        plt.figure(figsize=(8, 6))
        
        # Plot the block
        plt.plot(band_numbers, sum_smoothed, linestyle='-', color='b')
        plt.title(f"{title_prefix} - Block {idx + 1}")
        plt.xlabel("Band Number")
        plt.ylabel("Sum Closest to 1")
        
        # Save the plot in a file in the corresponding folder
        file_path = os.path.join(output_folder, f"{title_prefix}_block_{idx + 1}.png")
        plt.savefig(file_path)
        plt.close()  # Close the figure to free memory

def plot_results(results_up, results_down):
    """
    Generates and saves plots for consecutive blocks of results_up and results_down.
    """
    sigma_value = 1
    print("Saving plots for Spin Up...")
    plot_blocks(results_up, title_prefix="Spin_Up", sigma=sigma_value)
    
    print("Saving plots for Spin Down...")
    plot_blocks(results_down, title_prefix="Spin_Down", sigma=sigma_value)

# Call the main function passing your lists results_up and results_down
plot_results(results_up, results_down)











# Extract folder name from current directory
folder_name = os.path.basename(os.getcwd())
# Create 'localized' folder 
#localized_folder = f'../../../localized-defects/{folder_name}/'
localized_folder = 'localized-defects'
if not os.path.exists(localized_folder):
    os.makedirs(localized_folder)

    # Save the results
output_file = os.path.join(localized_folder, f'localized_{folder_name}.dat')

# Concatenate eigenval_infos.dat and vasprun_infos.dat
with open(output_file, 'w') as combined_file:
    # Read and write the content of eigenval_infos.dat
    combined_file.write(f"Defect: {folder_name}\n")
    combined_file.write(f"\nVBM = {VBM} eV\n")
    combined_file.write(f"CBM = {CBM} eV\n\n\n")
    combined_file.write("###########################################################\n")
    combined_file.write("                        EIGENVAL file                            \n")
    combined_file.write("###########################################################\n")
    with open(output_file_path, 'r') as eigenval_file:
        combined_file.write(eigenval_file.read())
    
    # Optionally add a separator for clarity
    combined_file.write("\n\n\n\n########################################################################\n")
    combined_file.write("                  vasprun.xml file (PROCAR information)\n")
    combined_file.write("########################################################################\n")
    
    # Read and write the content of vasprun_infos.dat
    with open('vasprun_infos.dat', 'r') as vasprun_file:
        combined_file.write(vasprun_file.read())

# Remove the eigenval_infos.dat and vasprun_infos.dat after finishing the calculations, 
files_to_remove = ['eigenval_infos.dat', 'vasprun_infos.dat']

for file in files_to_remove:
    try:
        os.remove(file)
#        print(f"The {file} has been removed.")
    except FileNotFoundError:
        print(f"The {file} file not found.")
    except Exception as e:
        print(f"Error deleting {file} file: {e}")
        
print(f"The localized-defects/localized_{folder_name}.dat file has been saved.")
