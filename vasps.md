---

# Steps for VASP calculations for phonons
Check [phonopy](https://phonopy.github.io/phonopy/).

## Activation
1. module spider phonopy
2. module load phonopy/2.16.3-foss-2022a
3. Create two folders with "mkdir relax phonon"

## Relaxation
1. Create INCAR_relax file
2. Introduce the POSCAR and jobfile
3. Create KPOINTS using command "makekpoints"
4. Create POTCAR using comand "makepot . Pt"
5. Use command "sub" for run your work
6. Use command "st" for check if your work is finished

## Features

- User authentication
- Responsive design
- Real-time data updates

## Technologies Used

- React
- Node.js
- Express
- MongoDB

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/projectname.git
   cd projectname
