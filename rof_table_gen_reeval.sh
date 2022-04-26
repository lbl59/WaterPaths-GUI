#!/bin/bash
#SBATCH -n 50 -N 5 -p normal
#SBATCH --job-name=rof_tables_reeval
#SBATCH --output=out_reeval/rof_tables_reeval.out
#SBATCH --error=out_reeval/rof_tables_reeval.err
#SBATCH --time=200:00:00
#SBATCH --mail-user=lbl59@cornell.edu
#SBATCH --mail-type=all

export OMP_NUM_THREADS=32

module load openmpi3/3.1.4
module spider py3-mpi4py
module spider py3-numpy/1.15.3

START="$(date +%s)"

mpirun python3 rof_tables_reeval.py

DURATION=$[ $(date +%s) - ${START} ]

echo ${DURATION}