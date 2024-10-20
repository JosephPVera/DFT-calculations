--- 
# Steps for VASP calculations: Relax, DOS and Band Structure
Check [VASP - UIO](https://wiki.uio.no/mn/kjemi/vaspwiki/index.php/Main_Page).

Steps for VASP calculations using **PBE** and **HSE06** pseudopotentials.

For use the commands as **vaspout**, **bandgap**, **toten**, **makekpoints**, **makepot**, **dosplot.py** and **bandplot.py** is necessary use scripts, check **/.../vasp/template/bin**.

---
# PBE pseudopotential
---

## Convergence test (Energy Cutoff)
1. Create **energy_cutoff** folder
   ```bash
   mkdir energy-cutoff
   ```
2. Create different folders 
   ```bash
   mkdir {200..900..50}
   ```
   
   - Introduce the same **POSCAR** and **jobfile** files in each folder.
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
     or all at once, using:
     ```bash
     for dir in */;do cd $dir; makepot . Pt Si; cd ../;done
     ```     
3. Use the following command for run your works
   ```bash
   sub
   ```
   or all at once, using
   ```bash
   for dir in */;do cd $dir; sub; cd ../;done 
   ```   
4. Use the following command for check if your works are finished
   ```bash
   st
   ```   
5. If all works are finished, use the following commands for check your outcomes 
   ```bash
   toten */OUTCAR
   vaspout */OUTCAR
   ```
   **toten** script allows us to check information about total energy, while **vaspout** script allows us to check information about MxForce, Drift, pressure and total energy.
6. Save your outcomes in a file with differents extension like .ods, .dat, .xlsx or .txt using the
   commands
   ```bash
   toten */OUTCAR > toten.dat
   vaspout */OUTCAR > vaspout.dat
   ```   

## Convergence test (K-density)
1. Create **k-density** folder
   ```bash
   mkdir k-density
   ```
2. Create different files  
   ```bash
   mkdir {2..9..1}
   ```
   - Introduce the same **POSCAR**, **POTCAR** and **jobfile** files in each folder.
     ```bash
     cp ../energy-cutoff/POSCAR ../energy-cutoff/POTCAR ../energy-cutoff/jobfile .
     ```
   - Use the **INCAR** file with the converged energy cutoff, from Convergence test (Energy Cutoff) section, in each folder.
   - Create **KPOINTS** file in each folder by changing the tag **k-density** following the name of the files: **{2..9..1}**, use the command
     ```bash
     makekpoints -d 2
     ```
     change the last number for different k-density. All at once, using:
     ```bash
     for dir in {2..9}; do cd "$dir"; makekpoints -d "$dir";cd ..;done
     ```
     check if it is correct
     ```bash
     grep k-density */KPOINTS
     ```
3. Run your works.
4. Check if your works are finished.
5. Repeat the steps 5 and 6 from Convergence test (Energy Cutoff) section.

## Creating folders
   ```bash
   mkdir PBE
   mkdir PBE/relax
   mkdir PBE/dos
   mkdir PBE/bs
   ```
## Relaxation
1. Enter to **relax** folder
   ```bash
   cd PBE/relax
   ```
2. Create **INCAR_relax** file, I recommend use the standart value for the energy cutoff **ENCUT  = 500** for the next calculations.
3. Use the same **POSCAR** and **jobfile** from Convergence test section.
4. Create **KPOINTS** file.   
5. Create **POTCAR** file.
6. Run your work.
7. Check your outcomes.

## Density of states (DOS)
0. This is a self-consistent calculation
1. Enter to **dos** folder
   ```bash
   cd ../dos
   ```
2. Create **INCAR_PBE_dos** file
3. Use the **CONTCAR** file from Relaxation section and change the name to **POSCAR**
   ```bash
   cp ../relax/CONTCAR POSCAR
   ```
4. Use the same **jobfile**, **KPOINTS** and **POTCAR** files from Relaxation section
   ```bash
   cp ../relax/jobfile ../relax/KPOINTS ../relax/POTCAR .
   ```
5. Run your work
6. Check your outcomes, using the following command you can check the information about 
   the bandgap (VBM and CBM)
   ```bash
   bandgap OUTCAR
   ```
7. Use the following command for plot the DOS
   ```bash
   dosplot.py
   ```
8. It is possible check the Local density of states (LDOS) using the command    
   ```bash
   dosplot.py --ldos 1
   ```
   change the last number according to your material.
9. Check your images 
   ```bash
   eog TDOS.png
   ```
