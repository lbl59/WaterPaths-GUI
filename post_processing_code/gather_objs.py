# organize output objectives by mean across RDMs and across solutions

import numpy as np

obj_names = ['REL_C', 'RF_C', 'INF_NPC_C', 'PFC_C', 'WCC_C', \
        'REL_D', 'RF_D', 'INF_NPC_D', 'PFC_D', 'WCC_D', \
        'REL_R', 'RF_R', 'INF_NPC_R', 'PFC_R', 'WCC_R', \
        'REL_reg', 'RF_reg', 'INF_NPC_reg', 'PFC_reg', 'WCC_reg']

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
Calculates the mean performance acorss all SOWs
'''
def mean_performance_across_rdms(objs_by_rdm_dir, N_RDMS, N_SOLNS):
    objs_matrix = np.zeros((N_SOLNS,20,N_RDMS), dtype='float')
    objs_means = np.zeros((N_SOLNS,20), dtype='float')

    for i in range(N_RDMS):
        filepathname = objs_by_rdm_dir + str(i) + '_sols0_to_' + str(N_SOLNS) + '.csv'
        objs_file = np.loadtxt(filepathname, delimiter=",")
        objs_matrix[:,:15,i] = objs_file

        objs_file_wRegional = minimax(N_SOLNS, objs_matrix[:,:,i])

        objs_matrix[:,:,i] = objs_file_wRegional

        array_has_nan = np.isnan(np.mean(objs_matrix[:,3,i]))
        if(array_has_nan == True):
            print('NaN found at RDM ', str(i))

    for n in range(N_SOLNS):
        for n_objs in range(20):
            objs_means[n,n_objs] = np.mean(objs_matrix[n,n_objs,:])

    return objs_means

'''
Calculates the mean performance acorss all SOWs
'''
def mean_performance_across_solns(objs_by_rdm_dir, N_RDMS, N_SOLNS):
    objs_matrix = np.zeros((N_SOLNS,20,N_RDMS), dtype='float')
    objs_means = np.zeros((N_RDMS,20), dtype='float')

    for i in range(N_RDMS):
        filepathname = objs_by_rdm_dir + str(i) + '_sols0_to_' + str(N_SOLNS) + '.csv'
        objs_file = np.loadtxt(filepathname, delimiter=",")
        objs_matrix[:,:15,i] = objs_file
        objs_file_wRegional = minimax(N_SOLNS, objs_matrix[:,:,i])

        objs_matrix[:,:,i] = objs_file_wRegional

        array_has_nan = np.isnan(np.mean(objs_matrix[:,3,i]))
        if(array_has_nan == True):
            print('NaN found at RDM ', str(i))

    for n in range(N_RDMS):
        for n_objs in range(20):
            objs_means[n,n_objs] = np.mean(objs_matrix[:,n_objs,n])

    return objs_means

# change number of solutions available depending on the number of solutions
# that you identified
N_SOLNS = 69
N_RDMS = 100

# change the filepaths
objs_by_rdm_dir = '/scratch/lbl59/blog/WaterPaths/output/Objectives_RDM'
objs_og_dir = '/scratch/lbl59/blog/WaterPaths/'

fileoutpath = '/scratch/lbl59/blog/WaterPaths/post_processing/'

fileoutpath_byRDMs = fileoutpath + 'meanObjs_acrossRDM.csv'
fileoutpath_bySoln = fileoutpath + 'meanObjs_acrossSoln.csv'

# should have shape (N_SOLNS, 20)
objs_byRDM = mean_performance_across_rdms(objs_by_rdm_dir, N_RDMS, N_SOLNS)
# should have shape (N_RDMS, 20)
objs_bySoln = mean_performance_across_solns(objs_by_rdm_dir, N_RDMS, N_SOLNS)

np.savetxt(fileoutpath_byRDMs, objs_byRDM, delimiter=",")
np.savetxt(fileoutpath_bySoln, objs_bySoln, delimiter=",")
