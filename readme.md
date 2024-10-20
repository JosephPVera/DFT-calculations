---

# Steps for VASP calculations: Phonons
Check [phonopy](https://phonopy.github.io/phonopy/).

## Folder Scheme

            
## Activation
1. Identify for the module
   ```bash
   module spider phonopy
2. Load the module
   ```bash
   module load phonopy/2.16.3-foss-2022a
3. Create the folders  
   ```bash
   mkdir relax phonon

## Relaxation
In **relax** file:
1. Create **INCAR_relax** file, example:
   ```bash
   # Electronic relaxation
   ALGO   = Normal    # Algorithm for electronic relaxation
   NELMIN = 4         # Minimum # of electronic steps
   NELM = 100         # sets the maximum number of electronic self-consistency steps 
   EDIFF  = 1E-8      # Accuracy for electronic groundstate
   ENCUT  = 500       # Cut-off energy for plane wave expansion
   PREC   = Accurate  # Low/Normal/Accurate
   LREAL  = .FALSE.   # Projection in reciprocal space
   ISMEAR = 1         # Smearing of partial occupancies
   SIGMA  = 0.1       # Smearing width
   ISPIN  = 2         # Spin polarization
   ISTART = 0         # Determines whether or not to read the WAVECAR
   ICHARG = 2         # Determines how VASP constructs the initial charge density

   # Ionic relaxation
   EDIFFG = -0.0005   # Defines the break condition for the ionic relaxation loop
   NSW    = 200       # Static high-accuracy calculation without relaxation
   IBRION = 2         # Algorithm for relaxing atomic positions 
   ISIF = 3           # 3 means relax volume, ISIF 2 or 0 relaxes only atoms, not lattice vectors
   ISYM = 1           # Determines the way VASP treats symmetry
   LWAVE = .FALSE.    # Determines whether the wavefunctions are saved in WAVECAR
   LCHARG = .FALSE.   # Determines whether the charge densities are saved in CHGCAR and CHG
   LMAXMIX = 4
 
   # Memory handling
   NPAR    = 4        # number of bands that are treated in parallel
   NCORE = 10         # number of compute cores that work on an individual orbital
   ```
2. Introduce the **POSCAR** and **jobfile** (HPC clusters use Slurm as workload manager and job scheduler).
3. Create **KPOINTS** file using command
   ```bash
   makekpoints
   ```
4. Create **POTCAR** using comand
   ```bash
   makepot . Pt
   ```
5. For run your work use the following command
   ```bash
   sub 
   ```   
8. Check if your work is finished
   ```bash
   st 
   ```   

## Phonon
In **phonon** file
1. Create INCAR_phonon file, example:
   ```bash
   ! Electronic relaxation
ALGO   = Normal    ! Algorithm for electronic relaxation
NELMIN = 4         ! Minimum # of electronic steps
NELM = 100
EDIFF  = 1E-8      ! Accuracy for electronic groundstate
ENCUT  = 500       ! Cut-off energy for plane wave expansion
PREC   = Accurate  ! Low/Normal/Accurate
LREAL  = .FALSE.   ! Projection in reciprocal space?
ISMEAR = 1         ! Smearing of partial occupancies.
SIGMA  = 0.1       ! Smearing width
ISTART = 0
ICHARG = 2

! Ionic relaxation
NSW    = 0         ! Static high-accuracy calculation without relaxation
IBRION = -1          ! Algorithm for relaxing atomic positions 
ISYM = 0
LWAVE = .FALSE.
LCHARG = .FALSE. 
LMAXMIX = 4
 
! Memory handling
NPAR    = 4
NCORE = 10 
  ``` 
3. Use the CONTCAR file from Relaxation section and change the name to POSCAR
4. Copy KPOINTS and POTCAR from Relaxation section

5. Use the command
   ```bash
   phonopy -d --dim="2 2 2
   ```
   for apply the transformation and create
   different POSCAR with finite-difference (displaced atoms) in the lattice parameter
   (Supercell method). It is possible to change the values "2 2 2" according to your material.
6. Now you will find POSCAR with different numbers: POSCAR-001, POSCAR-002
7. Create folders for each new POSCAR with 
   ```bash
   mkdir dis-001 dis-002
   ```
8. For each folder, example "dis-001"
   - Copy POSCAR-001 and change the name to POSCAR
   - Copy INCAR_phonon, KPOINTS, POTCAR and jobfile
   - Run your work 
   - Repeat the same steps for the other cases
9. In "phonon folder" use the command "phonopy -f dis-001/vasprun.xml dis-002/vasprun.xml" for
   create the FORCE_SETS file (this file is very important)

**IMPORTANT: NEXT CALCULATIONS PERFORM IN PHONON FOLDER**

### Density of states (DOS)
1. Create mesh.conf file with the command "touch mesh.conf"
   - Include name of the atoms of your material with the tag "ATOM_NAME"
   - Include the transformation applied with the tag "DIM"  
   - Include the Monkhorst-Pack scheme with the tag "MP"
2. Use the command "phonopy -p -s mesh.conf" for plot the DOS
3. Check the outcome with "evince total_dos.pdf"
4. Check information in "total_dos.dat" file

### Thermal properties
1. Use the command "phonopy -p -s -t  mesh.conf" for plot the thermal properties
2. Check the outcome with "evince thermal_properties.pdf"
3. Check information in "thermal_properties.yaml" file

### Partial Density of States (PDOS)
1. Create pdos.conf file
   - Include name of the atoms of your material with the tag "ATOM_NAME"
   - Include the transformation applied with the tag "DIM"  
   - Include the Monkhorst-Pack scheme with the tag "MP"
   - Include the Projected DOS with the tag "PDOS"
2. Use the command "phonopy -p -s pdos.conf" for plot the PDOS
3. Check the outcome with "evince partial_dos.pdf"
4. Check information in "projected_dos.dat" file

### Band structure
1. Create band.conf file
   - Include name of the atoms of your material with the tag "ATOM_NAME"
   - Include the transformation applied with the tag "DIM"
   - Include the high symmetry points with the tag "BAND"
   - Include the labels for the high symmetry points with the tag "BAND_LABELS"
2. Use the command "phonopy -p -s band.conf" for plot the band structure
3. Check the outcome with "evince band.pdf"
4. Check information in "band.yaml" file

### Non-analytical term correction (NAC)
0. Create a "nac" file
1. Create INCAR_nac
2. Copy POSCAR (primitice cell), KPOINTS, POTCAR and jobfile
3. Run your work
    
4. Use the command "phonopy-vasp-born > BORN" for create the BORN file
5. Now copy BORN file to phonon folder
6. Repeat the above commands adding "--nac" for calculate with the term correction
   - DOS:                "phonopy -p -s --nac mesh.conf"
   - Thermal properties: "phonopy -p -s -t --nac mesh.conf"
   - PDOS:               "phonopy -p -s --nac pdos.conf"
   - Band Structure:     "phonopy -p -s --nac band.conf"
7. For plot DOS and Band Structure at once
   - Create "band-dos.conf"
   - Use the command "phonopy -p -s --nac band-pdos.conf" for plot 
   - Check the outcome with "evince band_dos.pdf"

### Dielectric constant
1. Check the BORN file (second line is information about the dielectric tensor)
