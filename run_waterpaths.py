"""
The run_waterpaths.py file
Created on Sun Jan 09 2023 10:36

@author: Lillian Bei Jia Lau
"""
from mpi4py import MPI
import numpy as np
import pandas as pd
import subprocess, sys, time
import os

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
print('rank = ', rank)

input_parser_file=pd.read_csv('input_parser_file.txt', sep=" ", header=None)

N_REALIZATIONS = int(input_parser_file.iloc[0,1])

DATA_DIR = input_parser_file.iloc[1,1]
SOLS_FILE_NAME = input_parser_file.iloc[2,1]

SIM_TIME = int(input_parser_file.iloc[3,1])
C_VAL  = int(input_parser_file.iloc[4,1])
OMP_NUM_THREADS = int(input_parser_file.iloc[5,1])
N_RDMs = int(input_parser_file.iloc[6,1])
N_NODES = int(input_parser_file.iloc[9,1])
N_TASKS_PER_NODE = int(input_parser_file.iloc[10,1])
SOL_NUM_FIRST = int(input_parser_file.iloc[7,1])
SOL_NUM_LAST = int(input_parser_file.iloc[8,1])
OUTPUT_FREQ = int(input_parser_file.iloc[11,1])
NFE = int(input_parser_file.iloc[12,1])
SEED_NUM = int(input_parser_file.iloc[13,1])
MODE = input_parser_file.iloc[14,1]

N_TASKS = int(N_TASKS_PER_NODE * N_NODES)
N_RDMS_PER_TASK = int(N_RDMs/N_TASKS)

if C_VAL == 1 and MODE == "Optimize":
    command_run_rdm = "./waterpaths -T {} -t {} -r {} -d {} -C {} -O rof_tables_duOpt -e {} \
        -b true -n {} -o {} \
        -U TestFiles/rdm_utilities_test_problem_opt.csv \
        -W TestFiles/rdm_water_sources_test_problem_opt.csv \
        -P TestFiles/rdm_dmp_test_problem_opt.csv \
        -s {} -f {} -l {}\
        -p false".format(OMP_NUM_THREADS, SIM_TIME, N_REALIZATIONS, DATA_DIR, C_VAL , SEED_NUM, NFE, OUTPUT_FREQ, SOLS_FILE_NAME, SOL_NUM_FIRST, SOL_NUM_LAST)
    print(command_run_rdm)
    os.system(command_run_rdm)

elif C_VAL == 1 and MODE == "Re-evaluate":
    for i in range(N_RDMS_PER_TASK):
        current_RDM = rank + (N_TASKS * i)
        command_run_rdm = "./waterpaths -T {} -t {} -r {} -d {} -C {} -O rof_tables_duReeval/rdm_{} -e 0 \
            -U TestFiles/rdm_utilities_test_problem_opt.csv \
            -W TestFiles/rdm_water_sources_test_problem_opt.csv \
            -P TestFiles/rdm_dmp_test_problem_opt.csv \
            -R {} -s {} -f {} -l {}\
            -p false -c false".format(OMP_NUM_THREADS, SIM_TIME, N_REALIZATIONS, DATA_DIR, C_VAL, current_RDM, current_RDM, SOLS_FILE_NAME, SOL_NUM_FIRST, SOL_NUM_LAST)
        print(command_run_rdm)
        os.system(command_run_rdm)

elif C_VAL == -1 and MODE == "Optimize":
    command_run_rdm = "./waterpaths -T {} -t {} -r {} -d {} -C {} -O rof_tables_duOpt -e {} \
        -b true -n {} -o {} \
        -U TestFiles/rdm_utilities_test_problem_opt.csv \
        -W TestFiles/rdm_water_sources_test_problem_opt.csv \
        -P TestFiles/rdm_dmp_test_problem_opt.csv \
        -s {} -f {} -l {}\
        -p false".format(OMP_NUM_THREADS, SIM_TIME, N_REALIZATIONS, DATA_DIR, C_VAL, SEED_NUM, NFE, OUTPUT_FREQ, SOLS_FILE_NAME, SOL_NUM_FIRST, SOL_NUM_LAST)
    print(command_run_rdm)
    os.system(command_run_rdm)

elif C_VAL == -1 and MODE == "Re-evaluate":
    for i in range(N_RDMS_PER_TASK):
        current_RDM = rank + (N_TASKS * i)

        command_run_rdm = "./waterpaths -T {} -t {} -r {} -d {} -C {} -O rof_tables_duReeval/rdm_{} -e 0 \
            -U TestFiles/rdm_utilities_test_problem_reeval.csv \
            -W TestFiles/rdm_water_sources_test_problem_reeval.csv \
            -P TestFiles/rdm_dmp_test_problem_reeval.csv \
            -R {} -s {} -f {} -l {} \
            -p false -c false".format(OMP_NUM_THREADS, SIM_TIME, N_REALIZATIONS, DATA_DIR, C_VAL, current_RDM, current_RDM, SOLS_FILE_NAME, SOL_NUM_FIRST, SOL_NUM_LAST)
        print(command_run_rdm)
        os.system(command_run_rdm)

elif C_VAL == 0 and MODE == "Optimize":
    command_run_rdm = "./waterpaths -T {} -t {} -r {} -d {} -C {} -O rof_tables_duOpt -e {} \
        -b true -n {} -o {} \
        -U TestFiles/rdm_utilities_test_problem_opt.csv \
        -W TestFiles/rdm_water_sources_test_problem_opt.csv \
        -P TestFiles/rdm_dmp_test_problem_opt.csv \
        -s {} -f {} -l {}\
        -p false".format(OMP_NUM_THREADS, SIM_TIME, N_REALIZATIONS, DATA_DIR, C_VAL, SEED_NUM, NFE, OUTPUT_FREQ, SOLS_FILE_NAME, SOL_NUM_FIRST, SOL_NUM_LAST)
    print(command_run_rdm)
    os.system(command_run_rdm)

elif C_VAL == 0 and MODE == "Re-evaluate":
    for i in range(N_RDMS_PER_TASK):
        current_RDM = rank + (N_TASKS * i)

        command_run_rdm = "./waterpaths -T {} -t {} -r {} -d {} -C {} -O rof_tables_duReeval/rdm_{} -e 0 \
            -U TestFiles/rdm_utilities_test_problem_reeval.csv \
            -W TestFiles/rdm_water_sources_test_problem_reeval.csv \
            -P TestFiles/rdm_dmp_test_problem_reeval.csv \
            -R {} -s {} -f {} -l {} \
            -p false -c false".format(OMP_NUM_THREADS, SIM_TIME, N_REALIZATIONS, DATA_DIR, C_VAL, current_RDM, current_RDM, SOLS_FILE_NAME, SOL_NUM_FIRST, SOL_NUM_LAST)

        print(command_run_rdm)
        os.system(command_run_rdm)

elif C_VAL == 0 and MODE == "Reduced":
    command_run_rdm = "./waterpaths -T 4 -t 2344 -r 64 -d {} -s {} -m 0".format(DATA_DIR, SOLS_FILE_NAME)
    print(command_run_rdm)
    os.system(command_run_rdm)

comm.Barrier()
