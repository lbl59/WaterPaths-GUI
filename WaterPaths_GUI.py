"""
Created on Fri Jan 6 2023 11:25

@author: Lillian Bei Jia Lau
"""
# import all required libraries

from tkinter import *
import sys
import os
from pathlib import Path
from tkinter import font
import time

# create the main window
root = Tk()
root.title("WaterPaths")
# load an icon to use
p1 = PhotoImage(file = 'wpaths.png')
root.iconphoto(False, p1)
# set the initial size of the window, allow it to be resizeable
root.geometry("850x780")
root.resizable(True, True)

# data entry enabled here
#main_folder_location = Entry(root,text="Main Folder Location", width=10)

# Model setup frame
frame_setup_model = LabelFrame(root, text="1-Setup WaterPaths",
    bg='lightcyan', font=('HelvLight', 20), width=800, height=400)
frame_setup_model.grid(row=0,column=0,padx=10,pady=10, sticky="ew")
frame_setup_model.grid_propagate(True)

data_dir_label = Label(frame_setup_model, text="Data directory", justify=LEFT, bg='lightcyan').grid(sticky = W, row=1, column=0)
data_dir = Entry(frame_setup_model, width=60)
data_dir.grid(row=1, column=1, sticky=W)

gui_directory = os.getcwd()
gui_directory = gui_directory.replace(os.sep, '/') + '/'

data_dir.insert(0, gui_directory)

sols_filename_label = Label(frame_setup_model, text="Solution filename", anchor="w", justify=LEFT, bg='lightcyan').grid(sticky = W, row=2, column=0)
sols_filename = Entry(frame_setup_model, width=60)
sols_filename.grid(row=2, column=1, sticky = W)
sols_filename.insert(0, "sample_solutions.csv")

n_rdms_label = Label(frame_setup_model, text="Number of DU parameters", anchor="w", justify=LEFT, bg='lightcyan').grid(sticky = W, row=3, column=0)
n_rdms = Entry(frame_setup_model, width=10)
n_rdms.grid(row=3, column=1, sticky = W)
n_rdms.insert(0, "1000")

n_reals_label = Label(frame_setup_model, text="Number of hydroclimatic realizations", anchor="w", justify=LEFT, bg='lightcyan').grid(sticky = W, row=4, column=0)
n_reals = Entry(frame_setup_model, width=10)
n_reals.grid(row=4, column=1, sticky = W)
n_reals.insert(0, "500")

sim_time_label = Label(frame_setup_model, text="Simulation time (weeks)", anchor="w", justify=LEFT, bg='lightcyan').grid(sticky = W, row=5, column=0)
sim_time = Entry(frame_setup_model, width=10)
sim_time.grid(row=5, column=1, sticky = W)
sim_time.insert(0, "2344")

sol_first_label = Label(frame_setup_model, text="Fist solution to run", anchor="w", justify=LEFT, bg='lightcyan').grid(sticky = W, row=6, column=0)
sol_first = Entry(frame_setup_model, width=10)
sol_first.grid(row=6, column=1, sticky = W)
sol_first.insert(0, "0")

sol_last_label = Label(frame_setup_model, text="Last solution to run", anchor="w", justify=LEFT, bg='lightcyan').grid(sticky = W, row=7, column=0)
sol_last = Entry(frame_setup_model, width=10)
sol_last.grid(row=7, column=1, sticky = W)
sol_last.insert(0, "1000")

rof_dropdown = ["Export", "Import", "Nothing"]
gen_rof_tables = StringVar()
gen_rof_tables.set("Nothing")

rof_select = Label(frame_setup_model, text="Select ROF table mode", anchor="w", justify=LEFT,
    bg='lightcyan').grid(sticky = W, row=8, column=0)
rof_select = OptionMenu(frame_setup_model, gen_rof_tables , *rof_dropdown )
rof_select.grid(row=8, column=1, columnspan=1, sticky='W')
rof_select.config(width=10, font=['HelvLight','10', 'normal'], bg='lightcyan')

mode_dropdown = ["Optimize", "Re-evaluate", "Reduced"]
mode = StringVar()
mode.set("Reduced")

mode_select_label = Label(frame_setup_model, text="Select WaterPaths run mode", anchor="w", justify=LEFT,
    bg='lightcyan').grid(sticky = W, row=9, column=0)
mode_select = OptionMenu(frame_setup_model, mode , *mode_dropdown )
mode_select.grid(row=9, column=1, columnspan=1, sticky='W')
mode_select.config(width=10, font=['HelvLight','10', 'normal'], bg='lightcyan')
emptyLab_modeselect = Label(frame_setup_model, text="", justify=LEFT, bg='lightcyan').grid(row=9, column=0, sticky = 'W')

empty = Label(frame_setup_model, text=" ", anchor="w", justify=LEFT, bg='lightcyan').grid(sticky = W, row=10, column=0)

# Fill out machine specs
frame_opt_reeval = LabelFrame(root, text="2-Optimization/Re-Evaluation", padx=8, pady=8,
    bg='honeydew', font=('HelvLight', 20), width=750, height=350)
frame_opt_reeval.grid(row=1,column=0,padx=10,pady=10, sticky="ew")
frame_opt_reeval.grid_propagate(False)

task_alloc_explain = Label(frame_opt_reeval, text="Enter HPC submission requirements.",
    bg='honeydew', font=('HelvLight', 14)).grid(row=0, column=0)

n_threads_label = Label(frame_opt_reeval, text="Threads per core", anchor="w", justify=LEFT, bg='honeydew').grid(sticky = W, row=1, column=0)
n_threads = Entry(frame_opt_reeval, width=10)
n_threads.grid(row=1, column=1, sticky = W)
n_threads.insert(0, "64")

n_nodes_label = Label(frame_opt_reeval, text="Number of nodes", anchor="w", justify=LEFT, bg='honeydew').grid(sticky = W, row=2, column=0)
n_nodes = Entry(frame_opt_reeval, width=10)
n_nodes.grid(row=2, column=1, sticky = W)
n_nodes.insert(0, "1")

n_tasks_label = Label(frame_opt_reeval, text="Number of tasks per node", anchor="w", justify=LEFT, bg='honeydew').grid(sticky = W, row=3, column=0)
n_tasks = Entry(frame_opt_reeval, width=10)
n_tasks.grid(row=3, column=1, sticky = W)
n_tasks.insert(0, "1")

emptyLab_borg = Label(frame_opt_reeval, text="", justify=LEFT, bg='honeydew').grid(row=4, column=1, sticky = 'W')

borg_explain = Label(frame_opt_reeval, text="Only modify if running optimization.",
    bg='honeydew', font=('HelvLight', 14)).grid(row=4, column=0)

out_freq_label = Label(frame_opt_reeval, text="Output frequency", anchor="w", justify=LEFT, bg='honeydew').grid(sticky = W, row=5, column=0)
out_freq = Entry(frame_opt_reeval, width=10)
out_freq.grid(row=5, column=1, sticky = W)
out_freq.insert(0, "2500")

nfe_label = Label(frame_opt_reeval, text="Number of function evals", anchor="w", justify=LEFT, bg='honeydew').grid(sticky = W, row=6, column=0)
nfe = Entry(frame_opt_reeval, width=10)
nfe.grid(row=6, column=1, sticky = W)
nfe.insert(0, "125000")

n_seeds_label = Label(frame_opt_reeval, text="Seed number", anchor="w", justify=LEFT, bg='honeydew').grid(sticky = W, row=7, column=0)
n_seeds = Entry(frame_opt_reeval, width=10)
n_seeds.grid(row=7, column=1, sticky = W)
n_seeds.insert(0, "0")

def open_popup(text_out):
   top= Toplevel(root)
   top.geometry("600x120")
   top.title("WaterPaths")
   Label(top, text=text_out, justify=CENTER).place(x=10,y=10)

def install_req():
    '''
    Installs all Python libraries required to run the GUI
    Runs the WaterPaths makefile
    '''
    os.system("pip install -r requirements.txt")
    os.system("make gcc")
    text_out = "Program requirements installed. Do not run again."

    open_popup(text_out)

def write_params():
    path_output = gui_directory + 'output'

    if Path(path_output).exists() == False:
        os.mkdir(path_output, 0o666)

    #========== MAKE INPUTPARSERFILE HERE =====================================
    if os.path.exists("input_parser_file.txt"):
      os.remove("input_parser_file.txt")

    input_parser_file = open('input_parser_file.txt', 'w')

    #N_REALIZATIONS = int(n_reals.get())
    input_parser_file.writelines(['N_REALIZATIONS ', n_reals.get(), '\n'])
    input_parser_file.close()

    #DATA_DIR = data_dir.get()
    input_parser_file = open('input_parser_file.txt', 'a')
    input_parser_file.writelines(['DATA_DIR ', data_dir.get(), '\n'])
    input_parser_file.close()

    #SOLS_FILE_NAME = sols_filename.get()
    input_parser_file = open('input_parser_file.txt', 'a')
    input_parser_file.writelines(['SOLS_FILE_NAME ', sols_filename.get(), '\n'])
    input_parser_file.close()

    #SIM_TIME = int(sim_time.get())
    input_parser_file = open('input_parser_file.txt', 'a')
    input_parser_file.writelines(['SIM_TIME ', sim_time.get(), '\n'])
    input_parser_file.close()

    rof_generate = gen_rof_tables.get()
    C_VAL = 0
    if rof_generate == "Export":
        C_VAL = 1
    elif rof_generate == "Import":
        C_VAL = -1
    input_parser_file = open('input_parser_file.txt', 'a')
    input_parser_file.writelines(['C_VAL ', str(C_VAL), '\n'])
    input_parser_file.close()

    #OMP_NUM_THREADS = int(n_threads.get())
    input_parser_file = open('input_parser_file.txt', 'a')
    input_parser_file.writelines(['OMP_NUM_THREADS ', n_threads.get(), '\n'])
    input_parser_file.close()

    #N_RDMs = int(n_rdms.get())
    input_parser_file = open('input_parser_file.txt', 'a')
    input_parser_file.writelines(['N_RDMs ', n_rdms.get(), '\n'])
    input_parser_file.close()

    #SOL_NUM_FIRST = int(sol_first.get())
    input_parser_file = open('input_parser_file.txt', 'a')
    input_parser_file.writelines(['SOL_NUM_FIRST ', sol_first.get(), '\n'])
    input_parser_file.close()

    #SOL_NUM_LAST = int(sol_last.get())
    input_parser_file = open('input_parser_file.txt', 'a')
    input_parser_file.writelines(['SOL_NUM_LAST ', sol_last.get(), '\n'])
    input_parser_file.close()

    text_out = "WaterPaths parameters updated."

    open_popup(text_out)

reqs_button = Button(frame_setup_model, text="Install libraries", padx=10, pady=5, command=install_req,
                    fg='darkslategrey', bg='lightblue', font=['HelvLight', 12, 'bold']).grid(row=13, column=0, sticky='we')
emptyLab_reqs = Label(frame_setup_model, text="", justify=LEFT, bg='lightcyan').grid(row=14, column=0, sticky = 'W')

setup_button = Button(frame_setup_model, text="Setup WaterPaths", padx=10, pady=5, command=write_params,
                    fg='darkslategrey', bg='lightblue', font=['HelvLight', 12, 'bold']).grid(row=14, column=0, sticky='we')
emptyLab_setup = Label(frame_setup_model, text="", justify=LEFT, bg='lightcyan').grid(row=15, column=0, sticky = 'W')

'''
def run_waterpaths():

    os.system("sbatch ./run_waterpaths.sh")

    text_out = "Run submitted"
    open_popup(text_out)
'''

def make_inputfile():
    input_parser_file = open('input_parser_file.txt', 'a')

    #N_NODES = int(n_nodes.get())
    input_parser_file = open('input_parser_file.txt', 'a')
    input_parser_file.writelines(['N_NODES ', n_nodes.get(), '\n'])
    input_parser_file.close()

    #N_TASKS_PER_NODE = int(n_tasks.get())
    input_parser_file = open('input_parser_file.txt', 'a')
    input_parser_file.writelines(['N_TASKS_PER_NODE ', n_tasks.get(), '\n'])
    input_parser_file.close()

    #OUTPUT_FREQ = int(out_freq.get())
    input_parser_file = open('input_parser_file.txt', 'a')
    input_parser_file.writelines(['OUTPUT_FREQ ', out_freq.get(), '\n'])
    input_parser_file.close()

    #NFE = int(nfe.get())
    input_parser_file = open('input_parser_file.txt', 'a')
    input_parser_file.writelines(['NFE ', nfe.get(), '\n'])
    input_parser_file.close()

    #SEED_NUM = int(n_seeds.get())
    input_parser_file = open('input_parser_file.txt', 'a')
    input_parser_file.writelines(['SEED_NUM ', n_seeds.get(), '\n'])
    input_parser_file.close()

    input_parser_file = open('input_parser_file.txt', 'a')
    input_parser_file.writelines(['MODE ', mode.get()])
    input_parser_file.close()

    text_out = "HPC and Borg requirements specified.\n Input file created."

    open_popup(text_out)


emptyLab_wp = Label(frame_opt_reeval, text="", justify=LEFT, bg='honeydew').grid(row=8, column=0, sticky = 'we')

run_waterpaths = Button(frame_opt_reeval, text="Make input file", padx=10, pady=5, command=make_inputfile,
                           fg='darkgreen', bg='honeydew', font=('HelvLight',12, 'bold'), width=10).grid(row=11, column=0, sticky='we')

emptyLab_wp = Label(frame_opt_reeval, text="", justify=LEFT, bg='honeydew').grid(row=12, column=0, sticky = 'we')

root.mainloop()
