# -*- coding: utf-8 -*-
"""
Created on Thu May 12 22:29:04 2022

@author: lbl59
"""
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from copy import deepcopy
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
sns.set(style='white')

'''
FUNCTION to check whether performance criteria are met
'''
def check_satisficing(objs, objs_col, satisficing_bounds):
    meet_low = objs[:, objs_col] >= satisficing_bounds[0]
    meet_high = objs[:, objs_col] <= satisficing_bounds[1]

    meets_criteria = np.hstack((meet_low, meet_high)).all(axis=1)

    return meets_criteria

'''
FUNCTION to perform regional minimax
'''
def minimax(N_SOLNS, objs):
    for i in range(N_SOLNS):
        for j in range(5):
            if j == 0:
                objs[i,15] = np.min([objs[i,0],objs[i,5], objs[i,10]])
            else:
                objs[i, (j+15)] = np.max([objs[i,j],objs[i,j+5], objs[i,j+10]])
    return objs

'''
Name all file headers and compSol to be analyzed
'''
obj_names = ['REL_C', 'RF_C', 'INF_NPC_C', 'PFC_C', 'WCC_C', \
        'REL_D', 'RF_D', 'INF_NPC_D', 'PFC_D', 'WCC_D', \
        'REL_R', 'RF_R', 'INF_NPC_R', 'PFC_R', 'WCC_R', \
        'REL_reg', 'RF_reg', 'INF_NPC_reg', 'PFC_reg', 'WCC_reg']

dv_names = ['RT_C', 'RT_D', 'RT_R', 'TT_D', 'TT_R', 'LMA_C', 'LMA_D', 'LMA_R',\
            'RC_C', 'RC_D', 'RC_R', 'IT_C', 'IT_D', 'IT_R', 'IP_C', 'IP_D', \
            'IP_R', 'INF_C', 'INF_D', 'INF_R']

'''
Keys:
    CRE: Cary restriction efficiency
    DRE: Durham restriction efficiency
    RRE: Raleigh restriction efficiency
    DMP: Demand multiplier
    BTM: Bond term multiplier
    BIM: Bond interest rate multiplier
    IIM: Infrastructure interest rate multiplier
    EMP: Evaporation rate multplier
    STM: Streamflow amplitude multiplier
    SFM: Streamflow frequency multiplier
    SPM: Streamflow phase multiplier
'''

rdm_headers_dmp = ['CRE', 'DRE', 'RRE']
rdm_headers_utilities = ['DMP', 'BTM', 'BIM', 'IIM']
rdm_headers_inflows = ['STM', 'SFM', 'SPM']
rdm_headers_ws = ['EMP', 'CRR PTD', 'CRR CTD', 'LM PTD', 'LM CTD', 'AL PTD',
                  'AL CTD', 'D PTD', 'D CTD', 'NRR PTDD', 'NRR CTD', 'SCR PTD',
                  'SCT CTD', 'GC PTD', 'GC CTD', 'CRR_L PT', 'CRR_L CT',
                  'CRR_H PT', 'CRR_H CT', 'WR1 PT', 'WR1 CT', 'WR2 PT',
                  'WR2 CT', 'DR PT', 'DR CT', 'FR PT', 'FR CT']

rdm_headers_ws_drop = ['CRR PTD', 'CRR CTD', 'LM PTD', 'LM CTD', 'AL PTD',
                       'AL CTD', 'D PTD', 'D CTD', 'NRR PTDD', 'NRR CTD',
                       'SCR PTD', 'SCT CTD', 'GC PTD', 'GC CTD']

rdm_all_headers = ['CRE', 'DRE', 'RRE', 'DMP', 'BTM', 'BIM', 'IIM',
                   'STM', 'SFM', 'SPM', 'EMP', 'CRR_L PT', 'CRR_L CT',
                   'CRR_H PT', 'CRR_H CT', 'WR1 PT', 'WR1 CT', 'WR2 PT',
                   'WR2 CT', 'DR PT', 'DR CT', 'FR PT', 'FR CT']

all_headers = rdm_all_headers

utilities = ['Cary', 'Durham', 'Raleigh', 'Regional']

N_RDMS = 100
N_SOLNS = 69

'''
1 - Load DU factor files
'''
rdm_factors_directory = '/scratch/lbl59/blog/WaterPaths/TestFiles/'
rdm_dmp_filename = rdm_factors_directory + 'rdm_dmp_test_problem_reeval.csv'
rdm_utilities_filename = rdm_factors_directory + 'rdm_utilities_test_problem_reeval.csv'
rdm_inflows_filename = rdm_factors_directory + 'rdm_inflows_test_problem_reeval.csv'
rdm_watersources_filename = rdm_factors_directory + 'rdm_water_sources_test_problem_reeval.csv'

rdm_dmp = pd.read_csv(rdm_dmp_filename, sep=",", names=rdm_headers_dmp)
rdm_utilities = pd.read_csv(rdm_utilities_filename, sep=",", names=rdm_headers_utilities)
rdm_inflows = pd.read_csv(rdm_inflows_filename, sep=",", names=rdm_headers_inflows)
rdm_ws_full = np.loadtxt(rdm_watersources_filename, delimiter=",")
rdm_ws = pd.DataFrame(rdm_ws_full[:, :len(rdm_headers_ws)], columns=rdm_headers_ws)

rdm_ws = rdm_ws.drop(rdm_headers_ws_drop, axis=1)

dufs = pd.concat([rdm_dmp, rdm_utilities, rdm_inflows, rdm_ws], axis=1, ignore_index=True)
dufs.columns = rdm_all_headers
dufs_np = dufs.to_numpy()

duf_numpy = dufs_np[:100, :]

all_params = duf_numpy

'''
3 - Load objectives and robustness files
'''
out_directory = '/scratch/lbl59/blog/WaterPaths/post_processing/'

# objective values across all RDMs
objs_filename = out_directory + 'meanObjs_acrossSoln.csv'
objs_arr = np.loadtxt(objs_filename, delimiter=",")
objs_df = pd.DataFrame(objs_arr[:100, :], columns=obj_names)

'''
Determine the type of factor maps to plot.
'''
factor_names = all_headers

'''
Extract each utility's set of performance objectives and robustness
'''
Cary_all = objs_df[['REL_C', 'RF_C', 'INF_NPC_C', 'PFC_C', 'WCC_C']].to_numpy()
Durham_all = objs_df[['REL_D', 'RF_D', 'INF_NPC_D', 'PFC_D', 'WCC_D']].to_numpy()
Raleigh_all = objs_df[['REL_R', 'RF_R', 'INF_NPC_R', 'PFC_R', 'WCC_R']].to_numpy()
Regional_all = objs_df[['REL_reg', 'RF_reg', 'INF_NPC_reg', 'PFC_reg', 'WCC_reg']].to_numpy()

# Cary satisficing criteria
rel_C = check_satisficing(Cary_all, [0], [0.98, 1.0])
rf_C = check_satisficing(Cary_all, [1], [0.0, 0.1])
wcc_C = check_satisficing(Cary_all, [4], [0.0, 0.1])
satisficing_C = rel_C*rf_C*wcc_C
print('satisficing_C: ', satisficing_C.sum())

# Durham satisficing criteria
rel_D = check_satisficing(Durham_all, [0], [0.98, 1.0])
rf_D = check_satisficing(Durham_all, [1], [0.0, 0.1])
wcc_D = check_satisficing(Durham_all, [4], [0.0, 0.1])
satisficing_D = rel_D*rf_D*wcc_D
print('satisficing_D: ', satisficing_D.sum())

# Raleigh satisficing criteria
rel_R = check_satisficing(Raleigh_all, [0], [0.98,1.0])
rf_R = check_satisficing(Raleigh_all, [1], [0.0,0.1])
wcc_R = check_satisficing(Raleigh_all, [4], [0.0,0.1])
satisficing_R = rel_R*rf_R*wcc_R
print('satisficing_R: ', satisficing_R.sum())

# Regional satisficing criteria
rel_reg = check_satisficing(Regional_all, [0], [0.98, 1.0])
rf_reg = check_satisficing(Regional_all, [1], [0.0, 0.1])
wcc_reg = check_satisficing(Regional_all, [4], [0.0, 0.1])
satisficing_reg = rel_reg*rf_reg*wcc_reg
print('satisficing_reg: ', satisficing_reg.sum())

satisficing_dict = {'satisficing_C': satisficing_C, 'satisficing_D': satisficing_D,
                    'satisficing_R': satisficing_R, 'satisficing_reg': satisficing_reg}

utils = ['satisficing_C', 'satisficing_D', 'satisficing_R', 'satisficing_reg']

'''
6 - Fit a boosted tree classifier and extract important features
'''
for j in range(len(utils)):
    gbc = GradientBoostingClassifier(n_estimators=200,
                                     learning_rate=0.1,
                                     max_depth=3)

    # fit the classifier to each utility's sd
    # change depending on utility being analyzed!!
    criteria_analyzed = utils[j]
    df_to_fit = satisficing_dict[criteria_analyzed]
    gbc.fit(all_params, df_to_fit)

    feature_ranking = deepcopy(gbc.feature_importances_)
    feature_ranking_sorted_idx = np.argsort(feature_ranking)
    feature_names_sorted = [factor_names[i] for i in feature_ranking_sorted_idx]

    feature1_idx = len(feature_names_sorted) - 1
    feature2_idx = len(feature_names_sorted) - 2

    feature_figpath = '/scratch/lbl59/blog/WaterPaths/post_processing/BT_Figures/'
    print(feature_ranking_sorted_idx)

    feature_figname = feature_figpath + 'BT_' + criteria_analyzed + '.jpg'

    fig = plt.figure(figsize=(8, 8))
    ax = fig.gca()
    ax.barh(np.arange(len(feature_ranking)), feature_ranking[feature_ranking_sorted_idx])
    ax.set_yticks(np.arange(len(feature_ranking)))
    ax.set_yticklabels(feature_names_sorted)
    ax.set_xlim([0, 1])
    ax.set_xlabel('Feature ranking')
    plt.tight_layout()
    plt.savefig(feature_figname)

    '''
    7 - Create factor maps
    '''
    # select top 2 factors
    fm_figpath = '/scratch/lbl59/blog/WaterPaths/post_processing/BT_Figures/'
    fm_figname = fm_figpath + 'factor_map_' + criteria_analyzed + '.jpg'

    selected_factors = all_params[:, [feature_ranking_sorted_idx[feature1_idx],
                                     feature_ranking_sorted_idx[feature2_idx]]]
    gbc_2_factors = GradientBoostingClassifier(n_estimators=200,
                                               learning_rate=0.1,
                                               max_depth=3)

    # change this one depending on utility and compSol being analyzed
    gbc_2_factors.fit(selected_factors, df_to_fit)

    x_data = selected_factors[:, 0]
    y_data = selected_factors[:, 1]

    x_min, x_max = (x_data.min(), x_data.max())
    y_min, y_max = (y_data.min(), y_data.max())

    xx, yy = np.meshgrid(np.arange(x_min, x_max*1.001, (x_max-x_min)/100),
                         np.arange(y_min, y_max*1.001, (y_max-y_min)/100))

    dummy_points = list(zip(xx.ravel(), yy.ravel()))

    z = gbc_2_factors.predict_proba(dummy_points)[:,1]
    z[z<0] = 0
    z = z.reshape(xx.shape)

    fig_factormap = plt.figure(figsize = (10,8))
    ax_f = fig_factormap.gca()
    ax_f.contourf(xx, yy, z, [0, 0.5, 1], cmap='RdBu', alpha=0.6, vmin=0, vmax=1)

    ax_f.scatter(selected_factors[:,0], selected_factors[:,1],
                 c=df_to_fit, cmap='Reds_r', edgecolor='grey',
                 alpha=0.6, s=100, linewidths=0.5)


    ax_f.set_xlabel(factor_names[feature_ranking_sorted_idx[feature1_idx]], size=16)
    ax_f.set_ylabel(factor_names[feature_ranking_sorted_idx[feature2_idx]], size=16)
    ax_f.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08),
                fancybox=True, shadow=True, ncol=3, markerscale=0.5)

    plt.savefig(fm_figname)
