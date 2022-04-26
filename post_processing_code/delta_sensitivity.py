import sys
from SALib.analyze import delta
from SALib.util import read_param_file
import numpy as np
import pandas as pd

'''
Finds the upper and lower bounds of input parameters
'''
def find_bounds(input_file):
    bounds = np.zeros((input_file.shape[1],2), dtype=float)
    for i in range(input_file.shape[1]):
        bounds[i,0] = min(input_file[:,i])
        bounds[i,1] = max(input_file[:,i])

    return bounds
'''
Performs delta moment-independent sensitivity analysis
Source: https://github.com/SALib/SALib/tree/main/examples/delta
'''
def delta_sensitivity(dec_vars, measured_outcomes, names, mo_names, bounds, rdm, mode):
    X = dec_vars
    Y = measured_outcomes

    problem = {
        'num_vars': int(dec_vars.shape[1]),
        'names': names,
        'bounds': bounds
    }

    for i in range(measured_outcomes.shape[1]):
        mo_label = mo_names[i]
        filename = '../post_processing/delta_output_' + rdm + '/S1_' + mo_label + '.csv'
        S1 = delta.analyze(problem, X, Y[mo_label].values, num_resamples=10, conf_level=0.95, print_to_console=False)
        numpy_S1 = np.array(S1["S1"])
        fileout = pd.DataFrame([names, numpy_S1], index = None, columns = None)
        fileout.to_csv(filename, sep=",")

'''
0 - Name all file headers and compSol to be analyzed
'''
obj_names = ['REL_C', 'RF_C', 'INF_NPC_C', 'PFC_C', 'WCC_C', \
        'REL_D', 'RF_D', 'INF_NPC_D', 'PFC_D', 'WCC_D', \
        'REL_R', 'RF_R', 'INF_NPC_R', 'PFC_R', 'WCC_R', \
        'REL_reg', 'RF_reg', 'INF_NPC_reg', 'PFC_reg', 'WCC_reg']

dv_names = ['RT_C', 'RT_D', 'RT_R', 'TT_D', 'TT_R', 'LMA_C', 'LMA_D', 'LMA_R',\
            'RC_C', 'RC_D', 'RC_R', 'IT_C', 'IT_D', 'IT_R', 'IP_C', 'IP_D', \
            'IP_R', 'INF_C', 'INF_D', 'INF_R']

rdm_headers_dmp = ['Cary restr. eff', 'Durham restr. eff', 'Raleigh restr. eff']
rdm_headers_utilities = ['Demand growth\nmultiplier', 'Bond term\nmultiplier', \
                        'Bond interest\nrate multiplier', 'Infrastructure interest\nrate multiplier']
rdm_headers_ws = ['Streamflow amp', 'SCR PT', 'SCR CT', 'NRR PT', 'NRR CT', 'CR Low PT', 'CR Low CT',\
                  'CR High PT', 'CR High CT', 'WR1 PT', 'WR1 CT', 'WR2 PT', 'WR2 CT',\
                  'DR PT', 'DR CT', 'FR PT', 'FR CT']

duf_names = ['Cary restr. eff', 'Durham restr. eff', 'Raleigh restr. eff', 'Demand growth\nmultiplier',\
             'Bond term\nmultiplier', 'Bond interest\nrate multiplier', 'Infrastructure interest\nrate multiplier',\
             'Streamflow amp\nmultiplier', 'SCR PT\nmultiplier', 'SCR CT\nmultiplier', 'NRR PT\nmultiplier',\
             'NRR CT\nmultiplier', 'CR Low PT\nmultiplier', 'CR Low CT\nmultiplier', 'CR High PT\nmultiplier',\
             'CR High CT\nmultiplier', 'WR1 PT\nmultiplier', 'WR1 CT\nmultiplier', 'WR2 PT\nmultiplier',\
             'WR2 CT\nmultiplier', 'DR PT\nmultiplier', 'DR CT\nmultiplier', 'FR PT\nmultiplier', 'FR CT\nmultiplier',\
             'DR PT\nmultiplier', 'DR CT\nmultiplier', 'FR PT\nmultiplier', 'FR CT\nmultiplier']

utilities = ['Cary', 'Durham', 'Raleigh', 'Regional']

N_RDMS = 100
N_SOLNS = 69

'''
1 - Load DU factor files and DV files
'''
# change to your own filepath
rdm_factors_directory = '/scratch/lbl59/blog/WaterPaths/TestFiles/'
rdm_dmp_filename = rdm_factors_directory + 'rdm_dmp_test_problem_reeval.csv'
rdm_utilities_filename = rdm_factors_directory + 'rdm_utilities_test_problem_reeval.csv'
rdm_watersources_filename = rdm_factors_directory + 'rdm_water_sources_test_problem_reeval.csv'

rdm_dmp = pd.read_csv(rdm_dmp_filename, sep=",", names=rdm_headers_dmp)
rdm_utilities = pd.read_csv(rdm_utilities_filename, sep=",", names=rdm_headers_utilities)
rdm_ws_all = np.loadtxt(rdm_watersources_filename, delimiter=",")
rdm_ws = pd.DataFrame(rdm_ws_all[:,:17], columns=rdm_headers_ws)

dufs = pd.concat([rdm_dmp, rdm_utilities, rdm_ws], axis=1, ignore_index=True)
duf_numpy = dufs.to_numpy()

# change to your own filepath
dv_directory = '/scratch/lbl59/blog/WaterPaths/'
dv_filename = dv_directory + 'NC_dvs_all_noheader.csv'
dvs = np.loadtxt(dv_filename, delimiter=",")

'''
2 - Get bounds for DU factors and DVs
'''
duf_bounds = find_bounds(duf_numpy)
dv_bounds = find_bounds(dvs)

'''
3 - Load robustness file and objectives file
'''
# change to your own filepath
main_dir = '/scratch/lbl59/blog/WaterPaths/post_processing/'

robustness_filename = main_dir + 'robustness_100_SOWs.csv'
robustness_arr = np.loadtxt(robustness_filename, delimiter=",")
robustness_df = pd.DataFrame(robustness_arr, columns=utilities)

objs_mean_rdm_filename = main_dir + 'meanObjs_acrossRDM.csv'
objs_mean_rdm_arr = np.loadtxt(objs_mean_rdm_filename, delimiter=",")
objs_mean_rdm_df = pd.DataFrame(objs_mean_rdm_arr, columns=obj_names)

objs_mean_soln_filename = main_dir + 'meanObjs_acrossSoln.csv'
objs_mean_soln_arr = np.loadtxt(objs_mean_soln_filename, delimiter=",")
objs_mean_soln_df = pd.DataFrame(objs_mean_soln_arr, columns=obj_names)

# to change  depending on whether DV or DUF is being analyzed
dec_vars = duf_numpy[:100,:]
measured_outcomes = objs_mean_soln_df
names = duf_names
mo_names = obj_names
bounds = duf_bounds[:100,:]
rdm = 'DUF'
mode = 'objs'
###

delta_sensitivity(dec_vars, measured_outcomes, names, mo_names, bounds, rdm, mode)
