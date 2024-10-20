--- 
# Steps for VASP calculations: Relax, DOS and Band Structure
Check [VASP - UIO](https://wiki.uio.no/mn/kjemi/vaspwiki/index.php/Main_Page).

Steps for VASP calculations using **PBE** and **HSE06** pseudopotentials.

For use the commands as **vaspout**, **bandgap**, **toten**, **makekpoints**, **makepot**, **dosplot.py** and **bandplot.py** is necessary use scripts, check **/.../vasp/template/bin**.

# Creating the tree 
```bash
mkdir energy-cutoff k-density PBE HSE06
mkdir PBE/relax PBE/dos PBE/bs
mkdir HSE06/relax HSE06/dos HSE06/bs
```

---
# PBE pseudopotential
---

## Convergence test (Energy Cutoff)
1. Enter to **energy_cutoff** folder
   ```bash
   cd energy-cutoff
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
1. Enter to **k-density** folder
   ```bash
   cd k-density
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
   mkdir PBE/relax
   mkdir PBE/dos
   mkdir PBE/bs
   ```
## Relaxation
1. Enter to **relax** folder
   ```bash
   cd PBE/relax
   ```
2. Create **INCAR_PBE_relax** file, I recommend use the standart value for the energy cutoff **ENCUT  = 500** for the next calculations.
3. Use the same **POSCAR**, **POTCAR** and **jobfile** from Convergence test section.
4. Create **KPOINTS** file following the converged k-density.   
5. Run your work.
6. Check your outcomes.

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

## Band structure
0. This is a non-self-consistent calculation
1. Enter to **bs** folder
   ```bash
   cd ../bs
   ```
2. Create **INCAR_PBE_bs** file, include the new tag **ICHARG = 11**, last tag indicates the 
   non-self-consistent calculation
3. Copy **CHGCAR**, **POSCAR**, **POTCAR** and **jobfile** from DOS section
   ```bash
   cd ../dos/CHGCAR ../dos/POSCAR ../dos/jobfile ../dos/POTCAR .
   ```
4. Create **KPOINTS** file with the high symmetry points for the First Brillouin Zone (1BZ), here an example
   ```bash
   k-points along fcc high symmetry lines
   20     0  !                           # of points per line
   Line-mode
   reciprocal
   0.000  0.000  0.000  \Gamma
   0.500  0.000  0.500  X

   0.500  0.000  0.500  X
   0.500  0.250  0.750  W

   0.500  0.250  0.750  W
   0.375  0.375  0.750  K

   0.375  0.375  0.750  K
   0.000  0.000  0.000  \Gamma

   0.000  0.000  0.000  \Gamma
   0.500  0.500  0.500  L
 
   0.500  0.500  0.500  L
   0.625  0.250  0.625  U

   0.625  0.250  0.625  U
   0.500  0.250  0.750  W

   0.500  0.250  0.750  W
   0.500  0.500  0.500  L

   0.500  0.500  0.500  L
   0.375  0.375  0.750  K

   0.375  0.375  0.750  K
   0.625  0.250  0.625  U

   0.625  0.250  0.625  U
   0.500  0.000  0.500  X
   ```
5. Run your work
6. Plot the band structure with the command
   ```bash
   bandplot.py
   ```
7. Check your image 
   ```bash
   eog bandstruct.png
   ```

---
# HSE06 pseudopotential
---
# Creating folders
   ```bash
   mkdir HSE06
   mkdir HSE06/relax
   mkdir HSE06/dos
   mkdir HSE06/bs
   ```

## Relaxation
1. Enter to **relax** folder
   ```bash
   cd HSE06/relax
   ```
2. Create **INCAR_HSE06_relax** file, include the tags for hybrid calculations
   ```bash
   LHFCALC = .TRUE.        # specifies whether a Hartree-Fock/DFT hybrid functional type calculation is performed. 
   HFSCREEN = 0.2          # HF Screening parameter (0.2 for HSE06)
   AEXX = 0.25             # Fraction of exact exchange in a Hartree-Fock-type/hybrid-functional calculation
   AGGAX = 0.75            # parameter that multiplies the gradient correction in the GGA exchange functional
   Time = 0.4              # Timestep (0.4 for HSE06)
   ```
3. Introduce **POSCAR**, **KPOINTS**, **POTCAR** and **jobfile**, it can be copy from PBE calculations
   ```bash
   cp ../../PBE/dos/POSCAR ../../PBE/dos/KPOINTS ../../PBE/dos/POTCAR ../../PBE/dos/jobfile .
   ```
4. Run your work.
5. Check your outcomes.
