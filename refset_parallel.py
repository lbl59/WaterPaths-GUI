import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import seaborn as sns
from matplotlib import ticker
from matplotlib import cm
import matplotlib.colors as colors

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

normalized_objs = objs

# reliability
normalized_objs.iloc[:,0] = 1-(normalized_objs.iloc[:,0] - min(normalized_objs.iloc[:,0]))/(max(normalized_objs.iloc[:,0])-min(normalized_objs.iloc[:,0]))
normalized_objs.iloc[:,5] = 1-(normalized_objs.iloc[:,5] - min(normalized_objs.iloc[:,5]))/(max(normalized_objs.iloc[:,5])-min(normalized_objs.iloc[:,5]))
normalized_objs.iloc[:,10] = 1-(normalized_objs.iloc[:,10] - min(normalized_objs.iloc[:,10]))/(max(normalized_objs.iloc[:,10])-min(normalized_objs.iloc[:,10]))
normalized_objs.iloc[:,15] = 1-(normalized_objs.iloc[:,15] - min(normalized_objs.iloc[:,15]))/(max(normalized_objs.iloc[:,15])-min(normalized_objs.iloc[:,15]))

# restriction frequency
normalized_objs.iloc[:,1] = (normalized_objs.iloc[:,1] - min(normalized_objs.iloc[:,1]))/(max(normalized_objs.iloc[:,1])-min(normalized_objs.iloc[:,1]))
normalized_objs.iloc[:,6] = (normalized_objs.iloc[:,6] - min(normalized_objs.iloc[:,6]))/(max(normalized_objs.iloc[:,6])-min(normalized_objs.iloc[:,6]))
normalized_objs.iloc[:,11] = (normalized_objs.iloc[:,11] - min(normalized_objs.iloc[:,11]))/(max(normalized_objs.iloc[:,11])-min(normalized_objs.iloc[:,11]))
normalized_objs.iloc[:,16] = (normalized_objs.iloc[:,16] - min(normalized_objs.iloc[:,16]))/(max(normalized_objs.iloc[:,16])-min(normalized_objs.iloc[:,16]))

# infrastructure NPC
normalized_objs.iloc[:,2] = (normalized_objs.iloc[:,2] - min(normalized_objs.iloc[:,2]))/(max(normalized_objs.iloc[:,2])-min(normalized_objs.iloc[:,2]))
normalized_objs.iloc[:,7] = (normalized_objs.iloc[:,7] - min(normalized_objs.iloc[:,7]))/(max(normalized_objs.iloc[:,7])-min(normalized_objs.iloc[:,7]))
normalized_objs.iloc[:,12] = (normalized_objs.iloc[:,12] - min(normalized_objs.iloc[:,12]))/(max(normalized_objs.iloc[:,12])-min(normalized_objs.iloc[:,12]))
normalized_objs.iloc[:,17] = (normalized_objs.iloc[:,17] - min(normalized_objs.iloc[:,17]))/(max(normalized_objs.iloc[:,17])-min(normalized_objs.iloc[:,17]))

# peak financial cost
normalized_objs.iloc[:,3] = (normalized_objs.iloc[:,3] - min(normalized_objs.iloc[:,3]))/(max(normalized_objs.iloc[:,3])-min(normalized_objs.iloc[:,3]))
normalized_objs.iloc[:,8] = (normalized_objs.iloc[:,8] - min(normalized_objs.iloc[:,8]))/(max(normalized_objs.iloc[:,8])-min(normalized_objs.iloc[:,8]))
normalized_objs.iloc[:,13] = (normalized_objs.iloc[:,13] - min(normalized_objs.iloc[:,13]))/(max(normalized_objs.iloc[:,13])-min(normalized_objs.iloc[:,13]))
normalized_objs.iloc[:,18] = (normalized_objs.iloc[:,18] - min(normalized_objs.iloc[:,18]))/(max(normalized_objs.iloc[:,18])-min(normalized_objs.iloc[:,18]))

# worst-case cost
normalized_objs.iloc[:,4] = (normalized_objs.iloc[:,4] - min(normalized_objs.iloc[:,4]))/(max(normalized_objs.iloc[:,4])-min(normalized_objs.iloc[:,4]))
normalized_objs.iloc[:,9] = (normalized_objs.iloc[:,9] - min(normalized_objs.iloc[:,9]))/(max(normalized_objs.iloc[:,9])-min(normalized_objs.iloc[:,9]))
normalized_objs.iloc[:,14] = (normalized_objs.iloc[:,14] - min(normalized_objs.iloc[:,14]))/(max(normalized_objs.iloc[:,14])-min(normalized_objs.iloc[:,14]))
normalized_objs.iloc[:,19] = (normalized_objs.iloc[:,19] - min(normalized_objs.iloc[:,19]))/(max(normalized_objs.iloc[:,19])-min(normalized_objs.iloc[:,19]))

objs_names = ['REL', 'RF', 'INF_NPC', 'PFC', 'WCC']

objs_C = normalized_objs[['REL_C','RF_C','INF_NPC_C', 'PFC_C', 'WCC_C']]
objs_D = normalized_objs[['REL_D','RF_D','INF_NPC_D', 'PFC_D', 'WCC_D']]
objs_R = normalized_objs[['REL_R','RF_R','INF_NPC_R', 'PFC_R', 'WCC_R']]
objs_rg = normalized_objs[['REL_rg','RF_rg','INF_NPC_rg', 'PFC_rg', 'WCC_rg']]

objs_REL = normalized_objs[['REL_C','REL_D','REL_R', 'REL_rg']]
objs_RF = normalized_objs[['RF_C','RF_D','RF_R', 'RF_rg']]
objs_INF = normalized_objs[['INF_NPC_C','INF_NPC_D','INF_NPC_R', 'INF_NPC_rg']]
objs_PFC = normalized_objs[['PFC_C','PFC_D','PFC_R', 'PFC_rg']]
objs_WCC = normalized_objs[['WCC_C','WCC_D','WCC_R', 'WCC_rg']]

# decision variables
dvs_all = objs_dvs[['RT_C', 'RT_D', 'RT_R', 'TT_D', 'TT_R', 'JLA_C', \
                'JLA_D', 'JLA_R', 'RC_C', 'RC_D', 'RC_R', 'IT_C', \
                'IT_D', 'IT_R', 'IP_C', 'IP_D', 'IP_R', 'INF_C', 'INF_D', 'INF_R', \
                'INF_NPC_C', 'INF_NPC_D', 'INF_NPC_R']]

normalized_dvs = dvs_all

# restriction trigger
normalized_dvs.iloc[:,0] = (normalized_dvs.iloc[:,0] - min(normalized_dvs.iloc[:,0]))/(max(normalized_dvs.iloc[:,0])-min(normalized_dvs.iloc[:,0]))
normalized_dvs.iloc[:,1] = (normalized_dvs.iloc[:,1] - min(normalized_dvs.iloc[:,1]))/(max(normalized_dvs.iloc[:,1])-min(normalized_dvs.iloc[:,1]))
normalized_dvs.iloc[:,2] = (normalized_dvs.iloc[:,2] - min(normalized_dvs.iloc[:,2]))/(max(normalized_dvs.iloc[:,2])-min(normalized_dvs.iloc[:,2]))

# transfer trigger
normalized_dvs.iloc[:,3] = (normalized_dvs.iloc[:,3] - min(normalized_dvs.iloc[:,3]))/(max(normalized_dvs.iloc[:,3])-min(normalized_dvs.iloc[:,3]))
normalized_dvs.iloc[:,4] = (normalized_dvs.iloc[:,4] - min(normalized_dvs.iloc[:,4]))/(max(normalized_dvs.iloc[:,4])-min(normalized_dvs.iloc[:,4]))

# Lake Michael allocation
normalized_dvs.iloc[:,5] = (normalized_dvs.iloc[:,5] - min(normalized_dvs.iloc[:,5]))/(max(normalized_dvs.iloc[:,5])-min(normalized_dvs.iloc[:,5]))
normalized_dvs.iloc[:,6] = (normalized_dvs.iloc[:,6] - min(normalized_dvs.iloc[:,6]))/(max(normalized_dvs.iloc[:,6])-min(normalized_dvs.iloc[:,6]))
normalized_dvs.iloc[:,7] = (normalized_dvs.iloc[:,7] - min(normalized_dvs.iloc[:,7]))/(max(normalized_dvs.iloc[:,7])-min(normalized_dvs.iloc[:,7]))

# reserve fund contribution
normalized_dvs.iloc[:,8] = (normalized_dvs.iloc[:,8] - min(normalized_dvs.iloc[:,8]))/(max(normalized_dvs.iloc[:,8])-min(normalized_dvs.iloc[:,8]))
normalized_dvs.iloc[:,9] = (normalized_dvs.iloc[:,9] - min(normalized_dvs.iloc[:,9]))/(max(normalized_dvs.iloc[:,9])-min(normalized_dvs.iloc[:,9]))
normalized_dvs.iloc[:,10] = (normalized_dvs.iloc[:,10] - min(normalized_dvs.iloc[:,10]))/(max(normalized_dvs.iloc[:,10])-min(normalized_dvs.iloc[:,10]))

# insurance trigger
normalized_dvs.iloc[:,11] = (normalized_dvs.iloc[:,11] - min(normalized_dvs.iloc[:,11]))/(max(normalized_dvs.iloc[:,11])-min(normalized_dvs.iloc[:,11]))
normalized_dvs.iloc[:,12] = (normalized_dvs.iloc[:,12] - min(normalized_dvs.iloc[:,12]))/(max(normalized_dvs.iloc[:,12])-min(normalized_dvs.iloc[:,12]))
normalized_dvs.iloc[:,13] = (normalized_dvs.iloc[:,13] - min(normalized_dvs.iloc[:,13]))/(max(normalized_dvs.iloc[:,13])-min(normalized_dvs.iloc[:,13]))

# insurance payment
normalized_dvs.iloc[:,14] = (normalized_dvs.iloc[:,14] - min(normalized_dvs.iloc[:,14]))/(max(normalized_dvs.iloc[:,14])-min(normalized_dvs.iloc[:,14]))
normalized_dvs.iloc[:,15] = (normalized_dvs.iloc[:,15] - min(normalized_dvs.iloc[:,15]))/(max(normalized_dvs.iloc[:,15])-min(normalized_dvs.iloc[:,15]))
normalized_dvs.iloc[:,16] = (normalized_dvs.iloc[:,16] - min(normalized_dvs.iloc[:,16]))/(max(normalized_dvs.iloc[:,16])-min(normalized_dvs.iloc[:,16]))

# infrastructure trigger
normalized_dvs.iloc[:,17] = (normalized_dvs.iloc[:,17] - min(normalized_dvs.iloc[:,17]))/(max(normalized_dvs.iloc[:,17])-min(normalized_dvs.iloc[:,17]))
normalized_dvs.iloc[:,18] = (normalized_dvs.iloc[:,18] - min(normalized_dvs.iloc[:,18]))/(max(normalized_dvs.iloc[:,18])-min(normalized_dvs.iloc[:,18]))
normalized_dvs.iloc[:,19] = (normalized_dvs.iloc[:,19] - min(normalized_dvs.iloc[:,19]))/(max(normalized_dvs.iloc[:,19])-min(normalized_dvs.iloc[:,19]))

dvC_names = ['RT', 'JLA', 'RC', 'IT', 'IP', 'INF']
dv_names = ['RT', 'TT', 'JLA', 'RC', 'IT', 'IP', 'INF']

n_dvs_C = normalized_dvs[['RT_C', 'JLA_C', 'RC_C', 'IT_C', 'IP_C', 'INF_C', 'INF_NPC_C']]
n_dvs_D = normalized_dvs[['RT_D', 'TT_D', 'JLA_D', 'RC_D', 'IT_D', 'IP_D', 'INF_D', 'INF_NPC_D']]
n_dvs_R = normalized_dvs[['RT_R', 'TT_R', 'JLA_R', 'RC_R', 'IT_R', 'IP_R', 'INF_R','INF_NPC_R']]

dvs_C = objs_dvs[['RT_C', 'JLA_C', 'RC_C', 'IT_C', 'IP_C', 'INF_C', 'INF_NPC_C']]
dvs_D = objs_dvs[['RT_D', 'TT_D', 'JLA_D', 'RC_D', 'IT_D', 'IP_D', 'INF_D', 'INF_NPC_D']]
dvs_R = objs_dvs[['RT_R', 'TT_R', 'JLA_R', 'RC_R', 'IT_R', 'IP_R', 'INF_R','INF_NPC_R']]

dvs_C=dvs_C.sort_values(by=['INF_NPC_C'], ascending=False)
dvs_D=dvs_D.sort_values(by=['INF_NPC_D'], ascending=False)
dvs_R=dvs_R.sort_values(by=['INF_NPC_R'], ascending=False)

print(dvs_R)
dvs_rgT = normalized_dvs[['RT_C', 'RT_D', 'RT_R']]
dvs_TT = normalized_dvs[['TT_D', 'TT_R']]
dvs_JLA = normalized_dvs[['JLA_C', 'JLA_D', 'JLA_R']]
dvs_rgC = normalized_dvs[['RC_C', 'RC_D', 'RC_R']]
dvs_IT = normalized_dvs[['IT_C', 'IT_D', 'IT_R']]
dvs_IP = normalized_dvs[['IP_C', 'IP_D', 'IP_R']]
dvs_IP = normalized_dvs[['INF_C', 'INF_D', 'INF_R']]

## Parallel axis plots
# sharey=False indicates that all the subplot y-axes will be set to different values

x_objs = [i for i, _ in enumerate(objs_names)]
x_dvs = [i for i, _ in enumerate(dvC_names)]

fig1, ax1 = plt.subplots(1,len(x_dvs)-1, sharey=False, figsize=(20,4))

# enumerate through all the axes in the figure and plot the data
# only the first line of each
# blue for the nondominated solutions
# grey or everthing else
cmap = plt.get_cmap('pink_r')
cNorm = colors.Normalize(vmin=min(objs_INF['INF_NPC_C']), vmax=max(objs_INF['INF_NPC_C']))
scalarMap = cm.ScalarMappable(norm=cNorm, cmap=cmap)

for i, ax_i in enumerate(ax1):
    for d in range(len(n_dvs_C)):
        ax_i.plot(dvC_names, dvs_C.iloc[d, :6], color=scalarMap.to_rgba(objs_INF.iloc[d,0]), alpha=0.5, linewidth=3)
    ax_i.set_xlim([x_dvs[i], x_dvs[i+1]])

# function for setting ticks and tick_lables along the y-axis of each subplot
def set_ticks_for_axis(dim, ax_i, arr, ticks, rev):
    min_val = min(arr)
    max_val = max(arr)
    v_rgange = abs(max_val - min_val)
    step = v_rgange/float(ticks)
    tick_labels = [round(min_val + step*i, 2) for i in range(ticks)]
    if (rev == True):
        tick_labels.sort(reverse=True)
        print(tick_labels)

    norm_min = 0
    norm_range = 1.0
    norm_step =(norm_range/float(ticks-1))
    ticks = [round(norm_min + norm_step*i, 2) for i in range(ticks)]
    ax_i.set_ylim([0,1])
    ax_i.yaxis.set_ticks(ticks)
    ax_i.set_yticklabels(tick_labels)

# enumerating over each axis in fig2
for i in range(len(ax1)):
    ax1[i].xaxis.set_major_locator(ticker.FixedLocator([i]))  # set tick locations along the x-axis
    if i == 1:
        set_ticks_for_axis(i, ax1[i], dvs_C.iloc[:,1], ticks=5, rev=True)
    else:
        set_ticks_for_axis(i, ax1[i], dvs_C.iloc[:,i], ticks=5, rev=False)   # set ticks along the y-axis

# create a twin axis on the last subplot of fig2
# this will enable you to label the last axis with y-ticks
ax2 = plt.twinx(ax1[-1])
dim = len(ax1)
ax2.xaxis.set_major_locator(ticker.FixedLocator([x_dvs[-2], x_dvs[-1]]))
set_ticks_for_axis(dim, ax2, dvs_C.iloc[:,i], ticks=5, rev=False)
ax2.set_xticklabels([dv_names[-2], dv_names[-1]])

plt.subplots_adjust(wspace=0, hspace=0.5, left=0.1, right=0.85, bottom=0.1, top=0.9)
cbar=plt.colorbar(cm.ScalarMappable(norm=cNorm, cmap=cmap), ax=ax1)
cbar.set_label(r'$\leftarrow$ Infrastructure NPC')
ax1[0].set_ylabel("$\leftarrow$ Direction of preference ", fontsize=12)
plt.suptitle("Decision variables across Cary", fontsize=12, y=1.0)
plt.show()
