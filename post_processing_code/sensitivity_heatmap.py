import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid

sns.set_theme()

# change depending on compromise solution and whether its sensitivity to DUF or DVs
mode = 'DUF'
rot = 90    # if DV use 0; if DUF use 45
main_dir = '/scratch/lbl59/blog/WaterPaths/post_processing/delta_output_' + mode + '/'
c_filepath = main_dir + 'Cary.csv'
d_filepath = main_dir + 'Durham.csv'
r_filepath = main_dir + 'Raleigh.csv'
reg_filepath = main_dir + 'Regional.csv'

cary = pd.read_csv(c_filepath, index_col=False, header=0)
durham = pd.read_csv(d_filepath, index_col=False, header=0)
raleigh = pd.read_csv(r_filepath, index_col=False, header=0)
regional = pd.read_csv(reg_filepath, index_col=False, header=0)

savefig_dir = '/scratch/lbl59/blog/WaterPaths/post_processing/'
savefig_name = savefig_dir + 'dmi_heatmap_' + mode + '.svg'

grid_kws = {"height_ratios": (0.20, 0.20, 0.20, 0.20, .02), "hspace": 0.5}
f, (ax1, ax2, ax3, ax4, cbar_ax) = plt.subplots(5, figsize=(15, 20), gridspec_kw=grid_kws)
plt.subplots_adjust(top = 0.95, bottom = 0.05,
            hspace = 0, wspace = 0.05)

y_objs=['REL', 'RF', 'INPC', 'PFC', 'WCC']

x_dvs=['$RT_{C}$', '$RT_{D}$', '$RT_{R}$', '$TT_{D}$', '$TT_{R}$', '$LM_{C}$', '$LM_{D}$', '$LM_{R}$',\
                '$RC_{C}$', '$RC_{D}$', '$RC_{R}$', '$IT_{C}$', '$IT_{D}$', '$IT_{R}$', '$IP_{C}$', \
                '$IP_{D}$', '$IP_{R}$','$INF_{C}$', '$INF_{D}$', '$INF_{R}$']
x_dufs = ['Cary\nrestr. eff', 'Durham\nrestr. eff', 'Raleigh\nrestr. eff', 'Dem. growth\nmultiplier',\
             'Bond term\nmultiplier', 'Bond interest\nrate multiplier', 'Infra. interest\nrate multiplier',\
             'Streamflow amp\nmultiplier', 'SCR PT\nmultiplier', 'SCR CT\nmultiplier', 'NRR PT\nmultiplier',\
             'NRR CT\nmultiplier', 'CR Low PT\nmultiplier', 'CR Low CT\nmultiplier', 'CR High PT\nmultiplier',\
             'CR High CT\nmultiplier', 'WR1 PT\nmultiplier', 'WR1 CT\nmultiplier', 'WR2 PT\nmultiplier',\
             'WR2 CT\nmultiplier', 'DR PT\nmultiplier', 'DR CT\nmultiplier', 'FR PT\nmultiplier', 'FR CT\nmultiplier',\
             'DR PT\nmultiplier', 'DR CT\nmultiplier', 'FR PT\nmultiplier', 'FR CT\nmultiplier']

x_labs = []
if mode == 'DV':
    x_labs = x_dvs
elif mode == 'DUF':
    x_labs = x_dufs

plt.rc('xtick', labelsize=1)
plt.rc('ytick', labelsize=3)
plt.rc('axes', labelsize=5)
plt.rc('axes', titlesize=14)

#ax1 = fig.add_subplot(411)
ax1.set_title("Cary")
sns.heatmap(cary, linewidths=.05, cmap="YlOrBr", xticklabels=[],
    yticklabels=y_objs, ax=ax1, cbar=False)
ax1.set_yticklabels(y_objs, rotation=0)

#ax2 = fig.add_subplot(412)
ax2.set_title("Durham")
sns.heatmap(durham, linewidths=.05, cmap="YlOrBr", xticklabels=[],
    yticklabels=y_objs, ax=ax2, cbar=False)
ax2.set_yticklabels(y_objs, rotation=0)

#ax3 = fig.add_subplot(413)
ax3.set_title("Raleigh")
sns.heatmap(raleigh, linewidths=.05, cmap="YlOrBr", xticklabels=[],
    yticklabels=y_objs, ax=ax3, cbar=False)
ax3.set_yticklabels(y_objs, rotation=0)

#ax4 = fig.add_subplot(414, fontsize=10)
ax4.set_title("Regional")
ax4 = sns.heatmap(regional, linewidths=.05, cmap="YlOrBr", xticklabels=x_labs,
    yticklabels=y_objs, ax=ax4, cbar=True, cbar_ax=cbar_ax,
    cbar_kws={'orientation': 'horizontal'})     # change depending on whether analyzing DUF or DV
ax4.set_xticklabels(x_labs, rotation=rot, fontsize=10)
ax4.set_yticklabels(y_objs, rotation=0)

plt.savefig(savefig_name)
plt.show()
