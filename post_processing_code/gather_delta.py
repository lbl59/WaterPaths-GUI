"""
Created on Tue April 26 2022 16:12

@author: Lillian Bei Jia Lau

Gathers the delta sensitivity indices into files per utility
"""
import numpy as np
import pandas as pd

mode = 'DV'
main_dir = '/scratch/lbl59/blog/WaterPaths/post_processing/delta_output_' + mode + '/'
utilities = ['_C', '_D', '_R', '_reg']
objs = ['REL', 'RF', 'INF_NPC', 'PFC', 'WCC']
utilities_full = ['Cary', 'Durham', 'Raleigh', 'Regional']

dv_names = ['RT_C', 'RT_D', 'RT_R', 'TT_D', 'TT_R', 'LMA_C', 'LMA_D', 'LMA_R',\
            'RC_C', 'RC_D', 'RC_R', 'IT_C', 'IT_D', 'IT_R', 'IP_C', 'IP_D', \
            'IP_R', 'INF_C', 'INF_D', 'INF_R']

duf_names = ['Cary restr. eff', 'Durham restr. eff', 'Raleigh restr. eff', 'Demand growth\nmultiplier',\
             'Bond term\nmultiplier', 'Bond interest\nrate multiplier', 'Infrastructure interest\nrate multiplier',\
             'Streamflow amp\nmultiplier', 'SCR PT\nmultiplier', 'SCR CT\nmultiplier', 'NRR PT\nmultiplier',\
             'NRR CT\nmultiplier', 'CR Low PT\nmultiplier', 'CR Low CT\nmultiplier', 'CR High PT\nmultiplier',\
             'CR High CT\nmultiplier', 'WR1 PT\nmultiplier', 'WR1 CT\nmultiplier', 'WR2 PT\nmultiplier',\
             'WR2 CT\nmultiplier', 'DR PT\nmultiplier', 'DR CT\nmultiplier', 'FR PT\nmultiplier', 'FR CT\nmultiplier',\
             'DR PT\nmultiplier', 'DR CT\nmultiplier', 'FR PT\nmultiplier', 'FR CT\nmultiplier']

s1_dv_cary = np.zeros((len(objs), len(dv_names)), dtype=float)
s1_dv_durham = np.zeros((len(objs), len(dv_names)), dtype=float)
s1_dv_raleigh = np.zeros((len(objs), len(dv_names)), dtype=float)
s1_dv_regional = np.zeros((len(objs), len(dv_names)), dtype=float)

s1_dv_dict = {
    '_C': s1_dv_cary,
    '_D': s1_dv_durham,
    '_R': s1_dv_raleigh,
    '_reg': s1_dv_regional
}

s1_duf_cary = np.zeros((len(objs), len(duf_names)), dtype=float)
s1_duf_durham = np.zeros((len(objs), len(duf_names)), dtype=float)
s1_duf_raleigh = np.zeros((len(objs), len(duf_names)), dtype=float)
s1_duf_regional = np.zeros((len(objs), len(duf_names)), dtype=float)

s1_duf_dict = {
    '_C': s1_duf_cary,
    '_D': s1_duf_durham,
    '_R': s1_duf_raleigh,
    '_reg': s1_duf_regional
}


for i in range(len(utilities)):
    s1_util = []
    hdrs = []
    if mode == 'DV':
        s1_util = s1_dv_dict[utilities[i]]
        hdrs = dv_names
    elif mode == 'DUF':
        s1_util = s1_duf_dict[utilities[i]]
        hdrs = duf_names

    for j in range(len(objs)):
        curr_file = main_dir + 'S1_' + objs[j] + utilities[i] + '.csv'
        s1_util[j, :] = pd.read_csv(curr_file, sep=',', skiprows=2, header=None).iloc[0,1:]

    s1_util_df = pd.DataFrame(s1_util, columns=hdrs)
    out_filepath = main_dir + utilities_full[i] + '.csv'

    s1_util_df.to_csv(out_filepath, sep=',', index=False)
