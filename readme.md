--- 
# Steps for VASP calculations: Relax, DOS and Band Structure
Check [VASP - UIO](https://wiki.uio.no/mn/kjemi/vaspwiki/index.php/Main_Page).

Steps for VASP calculations using **PBE** and **HSE06** pseudopotentials.

For use the commands as **vaspout**, **bandgap**, **toten**, **makekpoints**, **makepot**, **dosplot.py** and **bandplot.py** is necessary use scripts, check **/.../vasp/template/bin**.

---
# PBE pseudopotential
---

## Convergence test (Energy Cutoff)
1. Create different folders 
   ```bash
   mkdir {200..900..50}
   ```
   
   - Introduce the same **POSCAR** and **jobfile** in each folder.
   - In **INCAR** file change the tag "**ENCUT**" following the name of the files: **{200..900..50}**
   - Create **KPOINTS** files in each folder using the command
     ```bash
     makekpoints
     ```
     or at once, using:
     ```bash
     for dir in */;do cd $dir; makekpoints; cd ../;done
     ```
   - Create **POTCAR** file using the comand 
     ```bash
     makepot . Pt
     ```
     change the element **Pt** according to your material. If you have two elements in the material use
     ```bash
     makepot . Pt Si
     ```
     or at once, using:
     ```bash
     for dir in */;do cd $dir; makepot . Pt Si; cd ../;done
     ```     
2. Use the following command for run your work
   ```bash
   sub
   ```
3. Use the following command for check if your work is finished
   ```bash
   st
   ```   
4. If all works are finished, use the following commands for check your outcomes 
   ```bash
   toten */OUTCAR
   vaspout */OUTCAR
   ```
   **toten** script allows us to check information about total energy, while **vaspout** script allows us to check information about MxForce, Drift, pressure and total energy.
5. Save your outcomes in a file with differents extension like .ods, .dat, .xlsx or .txt using the
   commands
   ```bash
   toten */OUTCAR > toten.dat
   vaspout */OUTCAR > vaspout.dat
   ```   
