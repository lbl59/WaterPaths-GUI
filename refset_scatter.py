import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import seaborn as sns
from matplotlib import ticker
from matplotlib import cm
import matplotlib.colors as colors
import matplotlib as mpl

objs_dvs = pd.read_csv('NC_dvs_objs.csv', sep=',', index_col=False)
cols = ['REL_C', 'RF_C', 'INF_NPC_C', 'PFC_C', 'WCC_C', \
        'REL_D', 'RF_D', 'INF_NPC_D', 'PFC_D', 'WCC_D', \
        'REL_R', 'RF_R', 'INF_NPC_R', 'PFC_R', 'WCC_R', \
        'REL_rg', 'RF_rg', 'INF_NPC_rg', 'PFC_rg', 'WCC_rg', \
        'RT_C', 'RT_D', 'RT_R', 'TT_D', 'TT_R', 'JLA_C', \
        'JLA_D', 'JLA_R', 'RC_C', 'RC_D', 'RC_R', 'IT_C', \
        'IT_D', 'IT_R', 'IP_C', 'IP_D', 'IP_R', 'INF_C', 'INF_D', 'INF_R']

objs_dvs[['REL_C','REL_D','REL_R', 'REL_rg']] = objs_dvs[['REL_C','REL_D','REL_R', 'REL_rg']]*100
objs_dvs[['PFC_C','PFC_D','PFC_R', 'PFC_rg']] = objs_dvs[['PFC_C','PFC_D','PFC_R', 'PFC_rg']]*100
objs_dvs[['WCC_C','WCC_D','WCC_R', 'WCC_rg']] = objs_dvs[['WCC_C','WCC_D','WCC_R', 'WCC_rg']]*100

# objectives
objs = objs_dvs[['REL_C','RF_C','INF_NPC_C', 'PFC_C', 'WCC_C', \
            'REL_D','RF_D','INF_NPC_D', 'PFC_D', 'WCC_D', \
            'REL_R','RF_R','INF_NPC_R', 'PFC_R', 'WCC_R', \
            'REL_rg','RF_rg','INF_NPC_rg', 'PFC_rg', 'WCC_rg']]

objs_names = ['REL', 'RF', 'INF_NPC', 'PFC', 'WCC']

objs_C = objs[['REL_C','RF_C','INF_NPC_C', 'PFC_C', 'WCC_C']]
objs_D = objs[['REL_D','RF_D','INF_NPC_D', 'PFC_D', 'WCC_D']]
objs_R = objs[['REL_R','RF_R','INF_NPC_R', 'PFC_R', 'WCC_R']]
objs_rg = objs[['REL_rg','RF_rg','INF_NPC_rg', 'PFC_rg', 'WCC_rg']]

objs_REL = objs[['REL_C','REL_D','REL_R', 'REL_rg']]
objs_RF = objs[['RF_C','RF_D','RF_R', 'RF_rg']]
objs_INF = objs[['INF_NPC_C','INF_NPC_D','INF_NPC_R', 'INF_NPC_rg']]
objs_PFC = objs[['PFC_C','PFC_D','PFC_R', 'PFC_rg']]
objs_WCC = objs[['WCC_C','WCC_D','WCC_R', 'WCC_rg']]
'''
# size is the worst-case cost
fig = plt.figure(figsize=(8,8))
ax = plt.axes(projection='3d')

# colorbar
cmap = mpl.cm.cool
norm = mpl.colors.Normalize(vmin=min(objs_rg['PFC_rg']), vmax=max(objs_rg['PFC_rg']))
cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, fraction=0.03, pad=0.02)

ax.scatter(objs_rg['REL_rg'], objs_rg['RF_rg'], objs_rg['INF_NPC_rg'], c=objs_rg['PFC_rg'], \
            cmap = cmap, s=objs_rg['WCC_rg']*2, marker='o', alpha = 0.5)

ax.set_xlabel('$\leftarrow$ Reliability (%)', size=12,labelpad=10)
ax.set_ylabel('$\leftarrow$ Restriction frequency (per 1000 SOWs)', size=12,labelpad=10)
ax.set_zlabel(r'Infra NPV (\$ mil) $\rightarrow$', size=12,labelpad=10)

ax.set_title('Objectives (regional)', size=14, pad=5)
cbar.set_label('PFC (%)')
plt.tight_layout()
plt.show()
'''
fig = plt.figure(figsize=(8,8))
ax = plt.axes(projection='3d')
ax.scatter(objs_rg['REL_rg'], objs_rg['RF_rg'], objs_C['WCC_C'], c='darkred', \
            s=30, marker='o', alpha = 0.5, label='Cary')
ax.scatter(objs_rg['REL_rg'], objs_rg['RF_rg'], objs_D['WCC_D'], c='darkturquoise', \
            s=30, marker='o', alpha = 0.5, label='Durham')
ax.scatter(objs_rg['REL_rg'], objs_rg['RF_rg'], objs_R['WCC_R'], c='orange', \
            s=30, marker='o', alpha = 0.5, label='Raleigh')

ax.set_xlabel(r'Regional reliability (%)$\rightarrow$ ', size=12,labelpad=10)
ax.set_ylabel('$\leftarrow$ Regional restriction frequency \n(per 1000 SOWs)', size=12,labelpad=10)
ax.set_zlabel(r'Regional worst-case cost \n(%)$\rightarrow$', size=12,labelpad=10)

ax.set_title("Comparing individual utility's INF NPC \nwith respect to REL and RF", size=14, pad=5)
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()
# decision variables
dvs_all = objs_dvs[['RT_W', 'RT_D', 'RT_F', 'TT_D', 'TT_F', 'LMA_W', \
            'LMA_D', 'LMA_F', 'RC_W', 'RC_D', 'RC_F', 'IT_W', \
            'IT_D', 'IT_F', 'IP_W', 'IP_D', 'IP_F', 'INF_W', 'INF_D', 'INF_F']]

dvs_W = dvs_all[['RT_W', 'LMA_W', 'RC_W', 'IT_W', 'IP_W', 'INF_W']]
dvs_D = dvs_all[['RT_D', 'TT_D', 'LMA_D', 'RC_D', 'IT_D', 'IP_D', 'INF_D']]
dvs_F = dvs_all[['RT_F', 'TT_F', 'LMA_F', 'RC_F', 'IT_F', 'IP_F', 'INF_F']]

dvs_RT = dvs_all[['RT_W', 'RT_D', 'RT_F']]
dvs_TT = dvs_all[['TT_D', 'TT_F']]
dvs_LMA = dvs_all[['LMA_W', 'LMA_D', 'LMA_F']]
dvs_RC = dvs_all[['RC_W', 'RC_D', 'RC_F']]
dvs_IT = dvs_all[['IT_W', 'IT_D', 'IT_F']]
dvs_IP = dvs_all[['IP_W', 'IP_D', 'IP_F']]
dvs_IP = dvs_all[['INF_W', 'INF_D', 'INF_F']]
'''
fig = plt.figure(figsize=(8,8))
ax = plt.axes(projection='3d')

# size is the worst-case cost
ax.scatter(objs_W.iloc[:99,0], objs_W.iloc[:99,1], objs_W.iloc[:99,2], c=objs_W.iloc[:99,3], \
            cmap = 'RdPu', s=objs_W.iloc[:99,4], label='Perturbed solns')
ax.scatter(objs_W.iloc[100,0], objs_W.iloc[100,1], objs_W.iloc[100,2], c='darkorchid', \
            s=objs_W.iloc[100,4], , marker = '*', label='FB171 soln')

ax.set_xlabel('WCC_W', size=12,labelpad=10)
ax.set_ylabel('WCC_D', size=12,labelpad=10)
ax.set_zlabel('WCC_F', size=12,labelpad=10)
cbar = plt.colorbar
cbar.set_label('Peak financial cost (%)')

legend_elements = [Line2D([0], [0], color='darkorchid', marker='*', label='FB171 soln'),
                   Line2D([0], [0], marker='o', color='purple', label='Perturbed solns',
                          markerfacecolor='g', markersize=15),
                   Patch(facecolor='orange', edgecolor='r',
                         label='Color Patch')]

ax.legend(loc='upper right')
ax.set_title('Worst-case financial cost of drought mitigation \n (% total annual revenue)', size=14, pad=5)
plt.tight_layout()
plt.show()
'''
