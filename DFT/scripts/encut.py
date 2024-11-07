#!/usr/bin/env python3
# Written by Joseph P.Vera
# 2024-11

import sys
import xml.etree.ElementTree as ET
import glob
import matplotlib.pyplot as plt
import numpy as np
import argparse  

"Plot the convergence for ENCUT"
"Usage:  ----> encut.py              # Default Realtive energy vs ENCUT \
         ----> encut.py --tot        # Total energy vs ENCUT \
         ----> encut.py --x 0.01 0.1 # Set X-range \
         ----> encut.py --y 0.01 0.1 # Set Y-range \
         ----> encut.py --cri        # Set the criteria for the relative energy vs ENCUT plot"

def extract_encut(filename):
    "Extract the ENCUT value from a vasprun.xml file."
    try:       
        encut_element = root.find(".//i[@name='ENCUT']") # keyword: <i name="ENCUT">    200.00000000</i>
        if encut_element is not None:
            encut_value = int(float(encut_element.text.strip()))
            return encut_value
        else:
            print(f"ENCUT not found in {filename}")
            return None
            
    except Exception as e:
        print(f"Error reading ENCUT from {filename}: {e}")
        return None

def extract_toten(filename):
    "Extract the last 'e_wo_entrp' energy from a vasprun.xml file."
    try:
        energies = root.findall(".//i[@name='e_wo_entrp']") # keyword: <i name="e_wo_entrp">    -17.00180199 </i>
        
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

def plot_convergence(encut_values, y_values, ylabel, show_criteria, criteria_value, x_range=None, y_range=None):
    plt.plot(encut_values, y_values, marker='o', linestyle='-', color='b')
    
    if x_range:
        plt.xlim(x_range)
    if y_range:
        plt.ylim(y_range)
    
    # Only include the criteria line if show_criteria is True
    if show_criteria:
        plt.axhline(criteria_value, linestyle='--', color='r', label=f'criteria = {criteria_value} eV')
        plt.legend()

    plt.xlabel('Energy cutoff (eV)')
    plt.ylabel(ylabel)
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

    args = parser.parse_args()

    # Use glob to search for all vasprun.xml files in subdirectories
    files = glob.glob("**/vasprun.xml", recursive=True)
    
    if not files:
        print("No vasprun.xml files found.")
        sys.exit(1)
    
    data = []

    for filename in files:
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            
            total_energy = extract_toten(root)
            encut = extract_encut(root)
            
            if total_energy is not None and encut is not None:
                data.append((encut, total_energy))
        except Exception as e:
            print(f"Error processing file {filename}: {e}")

    # Sort the data by the ENCUT value 
    data.sort(key=lambda x: x[0])
    
    # Calculate the relative differences from the total energy
    relatives = []
    for i in range(1, len(data)):
        relative = data[i][1] - data[i-1][1]
        relatives.append(relative)
    
    relatives.insert(0, float('nan'))

    # absolute value for the relative energies
    abs_relatives = [abs(relative) if not np.isnan(relative) else relative for relative in relatives]

    # Save the columns in list
    encut_values = [item[0] for item in data]
    relatives_values = abs_relatives
    total_energies = [item[1] for item in data]

    # Check if --tot command is passed
    if args.tot:
        ylabel = 'Total energy (eV)'
        y_values = total_energies # Plot total energy vs ENCUT
        show_criteria = False  # Don't show the criteria when using --tot
        name_fig = "toten-encut_convergence.png"
    else:
        ylabel = 'Relative energy (eV)'
        y_values = relatives_values # Plot Relative energy vs ENCUT
        show_criteria = True  # Show the criteria line for relative energies
        name_fig = "relative-encut_convergence.png"

    # Plot
    plot_convergence(encut_values, y_values, ylabel, show_criteria, args.cri, x_range=args.x, y_range=args.y)
