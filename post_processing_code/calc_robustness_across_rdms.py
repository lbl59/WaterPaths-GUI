# -*- coding: utf-8 -*-
"""
Created on Mon March 7 2022 16:12

@author: Lillian Bei Jia Lau

Calculates the fraction of RDMs over which each perturbed version of the solution meets all four satisficing criteria
"""
import numpy as np
import pandas as pd

obj_names = ['REL_C', 'RF_C', 'INF_NPC_C', 'PFC_C', 'WCC_C', \
        'REL_D', 'RF_D', 'INF_NPC_D', 'PFC_D', 'WCC_D', \
        'REL_R', 'RF_R', 'INF_NPC_R', 'PFC_R', 'WCC_R', \
        'REL_reg', 'RF_reg', 'INF_NPC_reg', 'PFC_reg', 'WCC_reg']

utilities = ['Cary', 'Durham', 'Raleigh', 'Regional']

'''
Performs regional minimax
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
For each rdm, identify if the perturbed solution version x satisfies the satisficing criteria
'''
def satisficing(df_objs):
    for i in range(4):
        df_objs['satisficing_C'] = (df_objs['REL_C'] >= 0.98).astype(int) *\
                                    (df_objs['WCC_C'] <= 0.10).astype(int) *\
                                    (df_objs['RF_C'] <= 0.10).astype(int)

        df_objs['satisficing_D'] = (df_objs['REL_D'] >= 0.98).astype(int) *\
                                    (df_objs['WCC_D'] <= 0.10).astype(int) *\
                                    (df_objs['RF_D'] <= 0.10).astype(int)

        df_objs['satisficing_R'] = (df_objs['REL_R'] >= 0.98).astype(int) *\
                                    (df_objs['WCC_R'] <= 0.10).astype(int) *\
                                    (df_objs['RF_R'] <= 0.10).astype(int)

    df_objs['satisficing_reg'] = np.max(df_objs.iloc[:, 20:23])
    return df_objs

def calc_robustness(objs_by_rdm_dir, N_RDMS, N_SOLNS):

    # matrix structure: (N_SOLNS, N_OBJS, N_RDMS)
    objs_matrix = np.zeros((N_SOLNS,20,N_RDMS), dtype='float')

    satisficing_matrix = np.zeros((N_SOLNS,4,N_RDMS), dtype='float')
    solution_robustness = np.zeros((N_SOLNS,4), dtype='float')

    for i in range(N_RDMS):
        # get one perturbed instance's behavior over all RDMs
        filepathname = objs_by_rdm_dir + str(i) + '_sols0_to_' + str(N_SOLNS) + '.csv'

        objs_file = np.loadtxt(filepathname, delimiter=",")

        objs_matrix[:,:15,i] = objs_file

        objs_file_wRegional = minimax(N_SOLNS, objs_matrix[:,:,i])

        objs_matrix[:,:,i] = objs_file_wRegional

        # NaN check
        array_has_nan = np.isnan(np.mean(objs_matrix[:,3,i]))
        if(array_has_nan == True):
            print('NaN found at RDM ', str(i))

    # for the perturbed instances
    for r in range(N_RDMS):

        df_curr_rdm = pd.DataFrame(objs_matrix[:, :, r], columns = obj_names)

        df_curr_rdm = satisficing(df_curr_rdm)
        satisficing_matrix[:N_SOLNS,:,r] = df_curr_rdm.iloc[:,20:24]

    for n in range(N_SOLNS):
        solution_robustness[n,0] = np.sum(satisficing_matrix[n,0,:])/N_RDMS
        solution_robustness[n,1] = np.sum(satisficing_matrix[n,1,:])/N_RDMS
        solution_robustness[n,2] = np.sum(satisficing_matrix[n,2,:])/N_RDMS

    solution_robustness[:,3] = np.min(solution_robustness[:,:3], axis=1)

    return solution_robustness

'''
Change number of solutions available depending on the number of solutions
that you identified and the number of SOWs that you are evaluating them over.
'''
N_RDMS = 100
N_SOLNS = 69

objs_by_rdm_dir = '/scratch/lbl59/blog/WaterPaths/output/Objectives_RDM'

fileoutpath_robustness = '/scratch/lbl59/blog/WaterPaths/post_processing/' + \
    'robustness_' + str(N_RDMS) + '_SOWs.csv'

robustness = calc_robustness(objs_by_rdm_dir, N_RDMS, N_SOLNS)

np.savetxt(fileoutpath_robustness, robustness, delimiter=",")
