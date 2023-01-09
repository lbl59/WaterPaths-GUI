#!/bin/bash
#SBATCH -n 1 -N 1 -p normal
#SBATCH --job-name=simple_reeval
#SBATCH --output=output/simple_reeval.out
#SBATCH --error=output/simple_reeval.err
#SBATCH --time=2:00:00
#SBATCH --mail-user=lbl59@cornell.edu
#SBATCH --mail-type=ALL

export OMP_NUM_THREADS=40
module load py3-mpi4py
module load py3-numpy

START="$(date +%s)"

mpirun python3 run_waterpaths.py

DURATION=$[ $(date +%s) - ${START} ]

echo ${DURATION}