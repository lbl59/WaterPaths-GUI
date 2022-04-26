#!/bin/bash
#SBATCH -n 50 -N 5 -p normal
#SBATCH --job-name=mordm_training_du_reeval
#SBATCH --output=out_reeval/mordm_training_du_reeval.out
#SBATCH --error=out_reeval/mordm_training_du_reeval.err
#SBATCH --time=200:00:00
#SBATCH --mail-user=lbl59@cornell.edu
#SBATCH --mail-type=all

export OMP_NUM_THREADS=32
module load openmpi3/3.1.4
module spider py3-numpy/1.15.3

START="$(date +%s)"

mpirun python3 run_du_reeval.py

DURATION=$[ $(date +%s) - ${START} ]

echo ${DURATION}