--- 
# Steps for VASP calculations: Relax, DOS and Band Structure
Check [VASP - UIO](https://wiki.uio.no/mn/kjemi/vaspwiki/index.php/Main_Page)

Steps for VASP calculations using PBE and HSE06 pseudopotentials.
For use the commands as **vaspout**, **bandgap**, **toten**, **makekpoints**, **makepot**, **dosplot.py** and **bandplot.py** is necessary use scripts, check **/.../vasp/template/bin**.

---
# PBE pseudopotential
---
## Convergence test (Energy Cutoff)
1. Create different files with mkdir {200..900..50}
   - Introduce the same POSCAR and jobfile
   - In INCAR file change the tag "ENCUT  = 500" following the name of the files {200..900..50}
   - Create KPOINTS using command "makekpoints"
   - Create POTCAR using comand "makepot . Pt", change the element according to your material. If
     you have two elements in the material use "makepot . Pt Si"
   
2. Use command "sub" for run your work
3. Use command "st" for check if your work is finished
   
4. If all works are finished, use commands "vaspout */OUTCAR", "bandgap */OUTCAR" or 
   "toten */OUTCAR" for check your outcomes
5. Save your outcomes in a file with differents extension like .ods, .dat, .xlsx or .txt using
   command "bandgap *dos/OUTCAR > bandgap.dat"
