#!/usr/bin/env python3
# Written by Joseph P.Vera
# 2024-11

import xml.etree.ElementTree as ET
import numpy as np

"Code for get the maximun force, pressure and drift. The maximum force and pressedure are extract form vasprun.xml file, while \
 drift is extract from OUTCAR file. OPTION: All information can also be found on OUTCAR with keywords: TOTAL-FORCE and total drift."

file_path = 'vasprun.xml'   
outcar_file = 'OUTCAR'

def extract_forces_and_stress(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    forces_data = []
    stress_data = []

    # Find the keyword <varray name="forces" >
    for varray in root.findall(".//varray[@name='forces']"):
        for v in varray.findall(".//v"):
            forces = list(map(float, v.text.split()))
            forces_data.append(forces)
    
    # Find the keyword <varray name="stress" >
    for varray in root.findall(".//varray[@name='stress']"):
        stress_matrix = []
        for v in varray.findall(".//v"):
            row = list(map(float, v.text.split()))
            stress_matrix.append(row)
        stress_data.append(stress_matrix)
    return forces_data, stress_data

def find_maximum_force(forces):
    max_force = float('-inf')  
    for force in forces:
        max_force_in_atom = max(force) 
        if max_force_in_atom > max_force:
            max_force = max_force_in_atom    
    return max_force

def find_pressure(stress_data):
    for matrix in stress_data:
        trace = matrix[0][0] + matrix[1][1] + matrix[2][2]
        pressure = trace/3   
    return pressure

def find_drift(outcar_file):
    with open(outcar_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if "total drift" in line.lower(): 
            parts = line.split()
            
            if len(parts) == 5:  
                x = float(parts[2])  
                y = float(parts[3]) 
                z = float(parts[4]) 
            
                drift = np.sqrt(x**2 + y**2 + z**2)
                
                return drift  

forces, stress = extract_forces_and_stress(file_path)
max_force = find_maximum_force(forces)
pressure = find_pressure(stress)
drift = find_drift(outcar_file)

print(f"{'MaxForce(eV/Å)':<20} {'Pressure(kB)':<20} {'Drift(eV/Å)':<14}")
print(f"{max_force:<20.4f} {pressure:<20.4f} {drift:<14.4f}")
