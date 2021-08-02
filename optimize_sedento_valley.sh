#!/bin/bash
#SBATCH -n 3 -N 3 -p normal
#SBATCH --job-name=sedento_valley_optimization
#SBATCH --output=output/sedento_valley_optimization.out
#SBATCH --error=error/sedento_valley_optimization.err
#SBATCH --time=04:00:00
#SBATCH --mail-user=lbl59@cornell.edu
#SBATCH --mail-type=all

DATA_DIR=/scratch/lbl59/blog/WaterPaths/
N_REALIZATIONS=1000
export OMP_NUM_THREADS=16
cd $SLURM_SUBMIT_DIR
mpirun ./waterpaths -T ${OMP_NUM_THREADS}\
  -t 2344 -r ${N_REALIZATIONS} -d ${DATA_DIR}\
  -C -1 -O rof_tables_test_problem/ -e 3\
  -U TestFiles/rdm_utilities_test_problem_opt.csv\
  -W TestFiles/rdm_water_sources_test_problem_opt.csv\
  -P TestFiles/rdm_dmp_test_problem_opt.csv\
  -b true -o 200 -n 1000