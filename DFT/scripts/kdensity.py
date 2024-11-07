#!/usr/bin/env python3
# Written by Joseph P.Vera
# 2024-11

import sys
import xml.etree.ElementTree as ET
import glob
import matplotlib.pyplot as plt
import numpy as np
import argparse  

"Plot the k-density convergence"
"Usage:  ----> kdensity.py              # Default Relative energy vs K-density \
         ----> kdensity.py --tot        # Total energy vs K-density \
         ----> kdensity.py --grid        # Relative energy vs K-grid \
         ----> kdensity.py --x 0.01 0.1 # Set X-range \
         ----> kdensity.py --y 0.01 0.1 # Set Y-range \
         ----> kdensity.py --cri        # Set the criteria for the relative energy vs K-density plot"

def extract_kgrid(root):
    "Extract the K-grid value from a vasprun.xml file."
    try:       
        kgrid_element = root.find(".//v[@name='divisions']")  # keyword: <v name="divisions">       5        5        5 </v>
        if kgrid_element is not None:
            # Remove extra spaces and replace them with a single 'x'
            kgrid_value = 'x'.join(kgrid_element.text.strip().split())
            return kgrid_value
        else:
            print(f"K-grid not found")
            return None
    except Exception as e:
        print(f"Error reading K-grid: {e}")
        return None

def extract_toten(filename):
    "Extract the last 'e_wo_entrp' energy from a vasprun.xml file."
    try:
        energies = root.findall(".//i[@name='e_wo_entrp']")  # keyword: <i name="e_wo_entrp">    -17.00180199 </i>
        
        # If any energies are found, take the last one
        if energies:
            last_energy = energies[-1].text.strip()  # Take the last value
            return float(last_energy)
        else:
            print(f"e_wo_entrp not found in {filename}")
            return None
            
    except Exception as e:
        print(f"Error reading e_wo_entrp from {filename}: {e}")
        return None

def plot_convergence(k_density_values, y_values, ylabel, show_criteria, criteria_value, show_k_density, x_range=None, y_range=None):
    plt.plot(k_density_values, y_values, marker='o', linestyle='-', color='b')
    
    if x_range:
        plt.xlim(x_range)
    if y_range:
        plt.ylim(y_range)
    
    # Only include the criteria line if show_criteria is True
    if show_criteria:
        plt.axhline(criteria_value, linestyle='--', color='r', label=f'criteria = {criteria_value} eV')
        plt.legend()

    if show_k_density:
        plt.xlabel('K-density (1/Å³)')
    else:
        plt.xlabel('K-grid')
    
    plt.ylabel(ylabel)
    
    if not show_k_density:
        plt.xticks(rotation=90) 
    
    plt.tight_layout()
    plt.savefig(name_fig, dpi=150)
    plt.show()
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and plot data from vasprun.xml files.")
    
    parser.add_argument('--x', type=float, nargs=2, metavar=('X_MIN', 'X_MAX'), help="Set the range for the x-axis")
    parser.add_argument('--y', type=float, nargs=2, metavar=('Y_MIN', 'Y_MAX'), help="Set the range for the y-axis")
    parser.add_argument('--cri', type=float, default=0.003, help="Set the criteria for the energy cutoff line (default: 0.003)")
    parser.add_argument('--tot', action='store_true', help="Plot total energy instead of relative energy")
    parser.add_argument('--grid', action='store_true', help="Plot K-grid instead of K-density")
    
    args = parser.parse_args()

    # Use glob to search for all vasprun.xml files in subdirectories
    files = glob.glob("**/vasprun.xml", recursive=True)
    
    if not files:
        print("No vasprun.xml files found.")
        sys.exit(1)
    
    data = []
    k_density_values = []
    kgrid_values = []
    total_energies = []
    relative_energies = []

    for filename in files:
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            
            total_energy = extract_toten(root)
            kgrid = extract_kgrid(root)
            
            if total_energy is not None and kgrid is not None:
                # Get the folder name to create k-density column
                folder_name = filename.split("/")[0] 
                k_density_values.append(folder_name)
                data.append((k_density_values[-1], kgrid, total_energy))
                
                kgrid_values.append(kgrid)
                total_energies.append(total_energy)
                
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
    
    # Sort the data by folder name
    data.sort(key=lambda x: int(x[0]))  
    
    # Calculate the relative energies
    relatives = []
    for i in range(1, len(data)):
        relative = data[i][2] - data[i-1][2]
        relatives.append(relative)
    
    relatives.insert(0, float('nan'))

    # Absolute value for relative energies
    abs_relatives = [abs(relative) if not np.isnan(relative) else relative for relative in relatives]

    # Save the columns in lists
    k_density_values = [item[0] for item in data]
    kgrid_values = [item[1] for item in data]
    relative_energies = abs_relatives
    total_energies = [item[2] for item in data]

    # Check if --tot command is passed
    if args.tot:
        ylabel = 'Total energy (eV)'
        y_values = total_energies  # Plot total energy vs ENCUT
        show_criteria = False  # Don't show the criteria when using --tot
        name_fig = "toten-kdensity_convergence.png"
        show_k_density = True  # Don't rotate if plotting total energy
    else:
        ylabel = 'Relative energy (eV)'
        y_values = relative_energies  # Plot Relative energy vs ENCUT
        show_criteria = True  # Show the criteria line for relative energies
        name_fig = "relative-kdensity_convergence.png"
        show_k_density = not args.grid  # If --grid is passed, don't show k-density
        
    # Plot
    plot_convergence(k_density_values if not args.grid else kgrid_values, y_values, ylabel, show_criteria, args.cri, show_k_density, x_range=args.x, y_range=args.y)
