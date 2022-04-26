# -*- coding: utf-8 -*-
"""
Created on Tues March 1 2022 16:16
@author: Lillian Bei Jia Lau
"""

from mpi4py import MPI
import numpy as np
import subprocess, sys, time
import os

# 5 nodes, 50 RDMs per node
# 16 tasks per node
# 5 RDMs per task
comm = MPI.COMM_WORLD
rank = comm.Get_rank() # up to 20 processes
print('rank = ', rank)

N_RDMs_needed = 100
N_REALIZATIONS = 100
N_RDM_PER_NODE = 20
N_TASKS_PER_NODE = 10 
N_RDM_PER_TASK = 2 # each task handles two RDMs
N_TASKS = 50 # rank ranges from 0 to 50

DATA_DIR = "/scratch/lbl59/blog/WaterPaths/"
SOLS_FILE_NAME = "NC_dvs_all_noheader.csv"
N_SOLS = 1

OMP_NUM_THREADS = 32

for i in range(N_RDM_PER_TASK):
    current_RDM = rank + (N_TASKS * i)

    command_gen_tables = "./waterpaths -T {} -t 2344 -r {} -d {} -C 1 -O rof_tables_reeval/rdm_{} -e 0 \
            -U TestFiles/rdm_utilities_test_problem_reeval.csv \
            -W TestFiles/rdm_water_sources_test_problem_reeval.csv \
            -P TestFiles/rdm_dmp_test_problem_reeval.csv \
            -s {} -f 0 -l {} -R {}\
            -p false".format(OMP_NUM_THREADS, N_REALIZATIONS, DATA_DIR, current_RDM, SOLS_FILE_NAME, N_SOLS, current_RDM)

    print(command_gen_tables)
    os.system(command_gen_tables)

comm.Barrier()
