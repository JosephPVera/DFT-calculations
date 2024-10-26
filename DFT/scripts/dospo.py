#!/usr/bin/env python3
# Written by Joseph P.Vera
# 2024-10

"Plot the DOS using the INCAR, OUTCAR and DOSCAR file"
"Example: dos.py 1 --s    # plot the s-orbital for the atom 1 \
          dos.py 1 --p    # plot the p-orbital for the atom 1 \
          dos.py 1 --d    # plot the d-orbital for the atom 1 \
          dos.py 1 --all  # plot the s,p,d-orbitals for the atom 1\
          dos.py 1 --tot --all # plot the total DOS and s,p,d-orbitals for the atom 1 \
          dos.py --tot    # plot the total DOS for the atom 1"  

import numpy as np
import matplotlib.pyplot as plt
import re
import sys

def get_value_from_incar(key, incar_file="INCAR", default=None):
    "Extract a specific value from the INCAR file"
    with open(incar_file, 'r') as file:
        for line in file:
            match = re.search(fr'{key}\s*=\s*(\d+)', line)
            if match:
                return int(match.group(1))
    return default

def get_fermi_energy(outcar_file="OUTCAR"):
    "Extract Fermi energy (E-fermi) from the OUTCAR file"
    fermi_energy = None
    with open(outcar_file, 'r') as file:
        for line in file:
            match = re.search(r'E-fermi\s*:\s*([-\d.]+)', line)
            if match:
                fermi_energy = float(match.group(1))
                break
    return fermi_energy
    
NEDOS = get_value_from_incar('NEDOS')
ISPIN = get_value_from_incar('ISPIN', default=1)
fermi_energy = get_fermi_energy()  


def plot_dos_total():
    "Plot total DOS"
    fig, ax = plt.subplots(figsize=(12, 8))
    if ISPIN == 1:
        dos_data = np.loadtxt("DOSCAR", unpack=True, usecols=(0, 1), skiprows=6, max_rows=NEDOS)
        energies = dos_data[0] - fermi_energy  
        spin_up = dos_data[1]          
        ax.plot(energies, spin_up, linestyle='-', color='r', label='Spin up')   
        ax.set_ylim(0.0, 2.5)
        
    elif ISPIN == 2:
        # Load file
        dos_data = np.loadtxt("DOSCAR", unpack=True, usecols=(0, 1, 2), skiprows=6, max_rows=NEDOS)
        energies = dos_data[0] - fermi_energy
        spin_up = dos_data[1]
        spin_down = dos_data[2] * -1  # Invert spin down for plotting
        ax.plot(energies, spin_up, linestyle='-', color='r', label='Spin up')
        ax.plot(energies, spin_down, linestyle='-', color='b', label='Spin down')
 


    ax.axvline(x=0, color='g', linestyle='dashed')
    ax.axhline(y=0, color='k', linestyle='-', linewidth=0.9)
    ax.set_ylabel('DOS (States/eV)')
    ax.set_xlabel('Energy (eV)')
    ax.legend()
    plt.savefig("total_dos.png", dpi=300, bbox_inches='tight')  
    plt.show()

def plot_dos_for_atom(atom_number, orbital_types=None):
    "Plot DOS for a specific atom"
    "data[1]: s-orbital (spin up), data[2]: s-orbital (spin down) \
    data[3]: p_x-orbital (spin up), data[5]: p_y-orbital (spin up), data[7]: p_z-orbital (spin up), \
    data[4]: p_x-orbital (spin down), data[6]: p_y-orbital (spin down), data[8]: p_z-orbital (spin down), \
    data[9]: d_xy-orbital (spin up), data[11]: d_yz-orbital (spin up), data[13]: d_xz-orbital (spin up), data[15]: d_{x²-y²}-orbital (spin up), data[17]: d_z²-orbital (spin up), \
    data[10]: d_xy-orbital (spin down), data[12]: d_yz-orbital (spin down), data[14]: d_xz-orbital (spin down), data[16]: d_{x²-y²}-orbital (spin dow), data[18]: d_z²-orbital (spin down)"
    start_line = NEDOS + 8 + (atom_number - 1) * (NEDOS + 1)
    data = np.loadtxt("DOSCAR", unpack=True, skiprows=start_line - 1, max_rows=NEDOS)

    energies = data[0] - fermi_energy

    fig, ax = plt.subplots(figsize=(12, 8))
    def plot_dos(x, y, color, label):
        ax.plot(x, y, linestyle='-', markersize=1, color=color, label=label)

    if orbital_types is None:
        orbital_types = ['s', 'p', 'd']  # Default to all orbitals

    if ISPIN == 1:
        # Plotting s-orbital (spin up and down)
        if 's' in orbital_types:
            s_orbital_up = data[1]
            plot_dos(energies, s_orbital_up, 'g', label='s-orbital')#f's-orbital (Spin up) Atom {atom_number}') 

        # Plotting p-orbital (spin up and down)
        if 'p' in orbital_types:
            p_orbital_up = data[2] + data[3] + data[4]  
            plot_dos(energies, p_orbital_up, 'b', label='p-orbital')#f'p-orbital (Spin up) Atom {atom_number}')

        # Plotting d-orbital (spin up and down)
        if 'd' in orbital_types:
            d_orbital_up = (data[5] + data[6] + data[7] + data[8] + data[9])
            plot_dos(energies, d_orbital_up, 'r', label='d-orbital')# f'd-orbital (Spin up) Atom {atom_number}')

    elif ISPIN == 2:
        # Plotting s-orbital (spin up and down)
        if 's' in orbital_types:
            s_orbital_up = data[1]
            s_orbital_down = data[2]
            plot_dos(energies, s_orbital_up, 'g', label='s-orbital')#f's-orbital (Spin up) Atom {atom_number}')             
            plot_dos(energies, s_orbital_down * -1, 'g', label=None)#, label=f's-orbital (Spin down) Atom {atom_number}')

        # Plotting p-orbital (spin up and down)
        if 'p' in orbital_types:
            p_orbital_up = data[3] + data[5] + data[7]  
            p_orbital_down = (data[4] + data[6] + data[8]) * -1 
            plot_dos(energies, p_orbital_up, 'b', label='p-orbital')#f'p-orbital (Spin up) Atom {atom_number}')
            plot_dos(energies, p_orbital_down, 'b', label=None)#, f'p-orbital (Spin down) Atom {atom_number}')

        # Plotting d-orbital (spin up and down)
        if 'd' in orbital_types:
            d_orbital_up = (data[9] + data[11] + data[13] + data[15] + data[17])
            d_orbital_down = ((data[10] + data[12] + data[14] + data[16] + data[18]) * -1)
            plot_dos(energies, d_orbital_up, 'r', label='d-orbital')# f'd-orbital (Spin up) Atom {atom_number}')
            plot_dos(energies, d_orbital_down, 'r', label=None)#, f'd-orbital (Spin down) Atom {atom_number}')    

    ax.axvline(x=0, color='k', linestyle='dashed')  
    ax.axhline(y=0, color='k', linestyle='-', linewidth=0.9) 
    ax.set_ylabel('DOS (States/eV)')
    ax.set_xlabel('Energy (eV)')
    ax.legend()
    plt.savefig(f"{orbital_types}-orbital_atom-{atom_number}.png",dpi=200, bbox_inches='tight')
    plt.show()

def plot_dos_combined(atom_number, orbital_types=None):
    "Plot both total DOS and DOS for a specific atom."
    fig, ax = plt.subplots(figsize=(12, 8))

    if ISPIN == 1:
        dos_data = np.loadtxt("DOSCAR", unpack=True, usecols=(0, 1), skiprows=6, max_rows=NEDOS)
        energies = dos_data[0] - fermi_energy  
        spin_up = dos_data[1]          
        ax.plot(energies, spin_up, linestyle='-', color='r', label='Total DOS')   
    
    elif ISPIN == 2:
        # Load file
        dos_data = np.loadtxt("DOSCAR", unpack=True, usecols=(0, 1, 2), skiprows=6, max_rows=NEDOS)
        energies = dos_data[0] - fermi_energy
        spin_up = dos_data[1]
        spin_down = dos_data[2] * -1  # Invert spin down for plotting
        ax.plot(energies, spin_up, linestyle='-', color='r', label='Spin up')
        ax.plot(energies, spin_down, linestyle='-', color='b', label='Spin down')
    
    # Now plot DOS for the specific atom
    start_line = NEDOS + 8 + (atom_number - 1) * (NEDOS + 1)
    data = np.loadtxt("DOSCAR", unpack=True, skiprows=start_line - 1, max_rows=NEDOS)
    energies = data[0] - fermi_energy
    
    def plot_dos(x, y, color, label):
        ax.plot(x, y, linestyle='-', markersize=1, color=color, label=label)

    if orbital_types is None:
        orbital_types = ['s', 'p', 'd']  # Default to all orbitals

    if ISPIN == 1:
        # Plotting s-orbital (spin up and down)
        if 's' in orbital_types:
            s_orbital_up = data[1]
            plot_dos(energies, s_orbital_up, 'g', label='s-orbital')#f's-orbital (Spin up) Atom {atom_number}')  

        # Plotting p-orbital (spin up and down)
        if 'p' in orbital_types:
            p_orbital_up = data[2] + data[3] + data[4]  
            plot_dos(energies, p_orbital_up, 'b', label='p-orbital')#f'p-orbital (Spin up) Atom {atom_number}')

        # Plotting d-orbital (spin up and down)
        if 'd' in orbital_types:
            d_orbital_up = (data[5] + data[6] + data[7] + data[8] + data[9])
            plot_dos(energies, d_orbital_up, 'r', label='d-orbital')# f'd-orbital (Spin up) Atom {atom_number}')

    elif ISPIN == 2:
        # Plotting s-orbital (spin up and down)
        if 's' in orbital_types:
            s_orbital_up = data[1]
            s_orbital_down = data[2]
            plot_dos(energies, s_orbital_up, 'g', label='s-orbital')#f's-orbital (Spin up) Atom {atom_number}')             
            plot_dos(energies, s_orbital_down * -1, 'g', label=None)#, label=f's-orbital (Spin down) Atom {atom_number}')

        # Plotting p-orbital (spin up and down)
        if 'p' in orbital_types:
            p_orbital_up = data[3] + data[5] + data[7]  
            p_orbital_down = (data[4] + data[6] + data[8]) * -1 
            plot_dos(energies, p_orbital_up, 'b', label='p-orbital')#f'p-orbital (Spin up) Atom {atom_number}')
            plot_dos(energies, p_orbital_down, 'b', label=None)#, f'p-orbital (Spin down) Atom {atom_number}')

        # Plotting d-orbital (spin up and down)
        if 'd' in orbital_types:
            d_orbital_up = (data[9] + data[11] + data[13] + data[15] + data[17])
            d_orbital_down = ((data[10] + data[12] + data[14] + data[16] + data[18]) * -1)
            plot_dos(energies, d_orbital_up, 'r', label='d-orbital')# f'd-orbital (Spin up) Atom {atom_number}')
            plot_dos(energies, d_orbital_down, 'r', label=None)#, f'd-orbital (Spin down) Atom {atom_number}')    

    ax.axvline(x=0, color='k', linestyle='dashed')  
    ax.axhline(y=0, color='k', linestyle='-', linewidth=0.9) 
    ax.set_ylabel('DOS (States/eV)')
    ax.set_xlabel('Energy (eV)')
    ax.legend()
    plt.savefig(f"tdos-s_p_d_orbitals_atom-{atom_number}.png", dpi=300, bbox_inches='tight') 
    plt.show()

if __name__ == '__main__':
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: dos.py atom_number --s/--p/--d/--all or dos.py --tot or dos.py atom_number --all --tot")
        sys.exit(1)

    # Parse arguments
    if '--tot' in sys.argv:
        if '--all' in sys.argv:
            atom_number = int(sys.argv[1]) 
            plot_dos_combined(atom_number)
        else:
            plot_dos_total()
    else:
        atom_number = int(sys.argv[1])
        if '--s' in sys.argv:
            plot_dos_for_atom(atom_number, orbital_types=['s'])
        elif '--p' in sys.argv:
            plot_dos_for_atom(atom_number, orbital_types=['p'])
        elif '--d' in sys.argv:
            plot_dos_for_atom(atom_number, orbital_types=['d'])
        elif '--all' in sys.argv:
            plot_dos_for_atom(atom_number, orbital_types=['s', 'p', 'd'])
