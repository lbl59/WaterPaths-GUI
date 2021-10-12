import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import seaborn as sns
from matplotlib import ticker
import matplotlib as mpl
from matplotlib import cm

## 3D scatter plots
NC_set = np.loadtxt('NC_output_MS_S3_N1000.set', delimiter=' ')

colnames = ['RT_C', 'RT_D', 'RT_R', 'TT_D', 'TT_R', 'JLA_C', \
        'JLA_D', 'JLA_R', 'RC_C', 'RC_D', 'RC_R', 'IT_C', \
        'IT_D', 'IT_R', 'IP_C', 'IP_D', 'IP_R', 'INF_C', 'INF_D', 'INF_R',\
        'REL_C', 'RF_C', 'INF_NPC_C', 'PFC_C', 'WCC_C', \
        'REL_D', 'RF_D', 'INF_NPC_D', 'PFC_D', 'WCC_D', \
        'REL_R', 'RF_R', 'INF_NPC_R', 'PFC_R', 'WCC_R']

NCset_df = pd.DataFrame(NC_set, columns=colnames, index=None)

# separate the decision variables from the objectives
# objectives
objs_all = NCset_df.iloc[:,20:]
dvs_all = NCset_df.iloc[:,:20]
# conduct minimax
def minimax(arr, rel=False):
    if rel==True:
        return min(arr)
    else:
        return max(arr)

objs_reg = np.zeros((NC_set.shape[0],5), dtype='float')
print(objs_reg.shape)
for i in range(objs_reg.shape[0]):
    objs_reg[i,0] = minimax(np.array([objs_all.iloc[i,0], objs_all.iloc[i,5], objs_all.iloc[i,10]]), rel=True)
    objs_reg[i,1] = minimax(np.array([objs_all.iloc[i,1], objs_all.iloc[i,6], objs_all.iloc[i,11]]))
    objs_reg[i,2] = minimax(np.array([objs_all.iloc[i,2], objs_all.iloc[i,7], objs_all.iloc[i,12]]))
    objs_reg[i,3] = minimax(np.array([objs_all.iloc[i,3], objs_all.iloc[i,8], objs_all.iloc[i,13]]))
    objs_reg[i,4] = minimax(np.array([objs_all.iloc[i,4], objs_all.iloc[i,9], objs_all.iloc[i,14]]))

objs_reg = pd.DataFrame(objs_reg, columns = ['REL_rg','RF_rg', 'INF_NPC_rg', 'PFC_rg', 'WCC_rg'])

NCset_df['REL_rg'] = objs_reg.iloc[:,0]
NCset_df['RF_rg'] = objs_reg.iloc[:,1]
NCset_df['INF_NPC_rg'] = objs_reg.iloc[:,2]
NCset_df['PFC_rg'] = objs_reg.iloc[:,3]
NCset_df['WCC_rg'] = objs_reg.iloc[:,4]

NCset_df.to_csv('NC_refset.csv', header=False, index=False)
NCset_df.to_csv('NC_dvs_objs.csv', index=False)
