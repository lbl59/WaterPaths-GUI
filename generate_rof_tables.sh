#!/bin/bash
#SBATCH -n 16 -N 2 -p normal
#SBATCH --job-name=gen_rof_tables
#SBATCH --output=output/gen_rof_tables.out
#SBATCH --error=error/gen_rof_tables.err
#SBATCH --time=04:00:00
#SBATCH --mail-user=lbl59@cornell.edu
#SBATCH --mail-type=all

export OMP_NUM_THREADS=16
cd $SLURM_SUBMIT_DIR
./waterpaths\
	-T ${OMP_NUM_THREADS}\
       	-t 2344\
       	-r 1000\
       	-d /scratch/lbl59/whats_acceptable/WaterPaths/\
       	-C 1\
	-m 0\
	-s sample_solutions.csv\
       	-O rof_tables_test_problem/\
       	-e 0\
       	-U TestFiles/rdm_utilities_test_problem_opt.csv\
       	-W TestFiles/rdm_water_sources_test_problem_opt.csv\
       	-P TestFiles/rdm_dmp_test_problem_opt.csv\
	-p false