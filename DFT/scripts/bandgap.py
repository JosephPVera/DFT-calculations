#!/usr/bin/env python
# Written by Joseph P.Vera
# 2024-10

from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.bandstructure import BandStructure

vasprun = Vasprun("vasprun.xml")  
band_structure = vasprun.get_band_structure()

cbm = band_structure.get_cbm()
vbm = band_structure.get_vbm()

if cbm:
    print("Conduction Band Minimum (CBM):")
    print(f"  Energy: {cbm['energy']} eV")
else:
    print("CBM not found (possibly metallic).")

if vbm:
    print("\nValence Band Maximum (VBM):")
    print(f"  Energy: {vbm['energy']} eV")
else:
    print("\nVBM not found (possibly metallic).")

if cbm and vbm:
    band_gap = cbm["energy"] - vbm["energy"]
    print(f"\nBand Gap: {band_gap} eV")
else:
    print("\nNo band gap (metallic material).")