# -*- coding: utf-8 -*-
"""
Created on Tues March 1 2022 16:16

@author: Lillian Bei Jia Lau
"""

from mpi4py import MPI
import numpy as np
import subprocess, sys, time
import os

N_RDMs_needed = 100  # N_TASKS_PER_NODE * N_RDM_PER_TASK * num nodes
N_REALIZATIONS = 100
N_RDM_PER_NODE = 20
N_TASKS_PER_NODE = 10 # rank ranges from 0 to 15
N_RDM_PER_TASK = 2 # each task handles five RDMs
N_TASKS = 50

comm = MPI.COMM_WORLD
rank = comm.Get_rank() # up to 20 processes
print('rank = ', rank)

DATA_DIR = "/scratch/lbl59/blog/WaterPaths/"
SOLS_FILE_NAME = "NC_dvs_all_noheader.csv"
N_SOLS = 69
OMP_NUM_THREADS = 32

for i in range(N_RDM_PER_TASK):
    current_RDM = rank + (N_TASKS * i)

    command_run_rdm = "./waterpaths -T {} -t 2344 -r {} -d {} -C -1 -O rof_tables_reeval/rdm_{} -e 0 \
            -U TestFiles/rdm_utilities_test_problem_reeval.csv \
            -W TestFiles/rdm_water_sources_test_problem_reeval.csv \
            -P TestFiles/rdm_dmp_test_problem_reeval.csv \
            -s {} -R {} -f 0 -l 69\
            -p false".format(OMP_NUM_THREADS, N_REALIZATIONS, DATA_DIR, \
                    current_RDM , SOLS_FILE_NAME, current_RDM)

    print(command_run_rdm)
    os.system(command_run_rdm)

comm.Barrier()
