from scipy.stats import kendalltau

import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 
sns.set_theme(style="white")

fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(10,5))

model_name = 'dctr'

df_data = []

ref = ['XSqrA_M', 'BM25', 'Baseline', 'Tf', 'Dl', 'Null']
for k in [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,50]:

    df = pd.read_csv('experimental_results/' + model_name + '.ll.lrm.' + str(k) + '.csv')
    s = 20
    t = 10
    for _s in range(1, s+1):
        for _t in range(1, t+1):
            sys_rank = list(df[(df['sessions'] == _s) & (df['trial'] == _t)].sort_values(by='loglikelihood', ascending=False)['system'])
            corr, _ = kendalltau(ref, sys_rank)
            df_data.append({
                'queries': k,
                'sessions': _s,
                'trial': _t,
                'ktau': corr
            })
_df = pd.DataFrame(df_data)
sns.heatmap(_df.groupby(['queries', 'sessions']).mean().reset_index().pivot("queries", "sessions", "ktau"),
            square=True,
            cmap="Greens",
            ax=axes[0],cbar=False, vmin=.0, vmax=1.0)
axes[0].set_ylabel('DCTR \n Number of Queries')
axes[0].set_title('LRM')
axes[0].set_xlabel('Number of Sessions')

df_data = []
ref = [.4, .45, .5, .55, .6,  .65,  .7, .75, .8, .85, .9, .95, 1]
for k in [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,50]:
    df = pd.read_csv('experimental_results/' + model_name + '.ll.irm.' + str(k) + '.csv')
    s = 20
    t = 10
    for _s in range(1, s+1):
        for _t in range(1, t+1):
            sys_rank = list(df[(df['sessions'] == _s) & (df['trial'] == _t)].sort_values(by='loglikelihood', ascending=False)['weight'])
            corr, _ = kendalltau(ref, sys_rank)
            df_data.append({
                'queries': k,
                'sessions': _s,
                'trial': _t,
                'ktau': corr
            })
_df = pd.DataFrame(df_data)
cbar_ax = fig.add_axes([.91, .2, .025, .6])
sns.heatmap(_df.groupby(['queries', 'sessions']).mean().reset_index().pivot("queries", "sessions", "ktau"),
            square=True,
            cmap="Greens",
            ax=axes[1], cbar_ax = cbar_ax, cbar=True, vmin=.0, vmax=1.0)
axes[1].set_ylabel('')
axes[1].set_title('IRM')
axes[1].set_xlabel('Number of Sessions')

plt.savefig('experimental_results/figures/' + model_name + '.ktau.ll.heatmaps.pdf', format='pdf', bbox_inches='tight')

################################################################################
##### DCM + SDBN ###############################################################

fig, axes = plt.subplots(nrows=2, ncols=2, sharey=True, figsize=(5,5))

model_name = 'dcm'

df_data = []
ref = ['XSqrA_M', 'BM25', 'Baseline', 'Tf', 'Dl', 'Null']
for k in [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,50]:

    df = pd.read_csv('experimental_results/' + model_name + '.ll.lrm.' + str(k) + '.csv')
    s = 20
    t = 10
    for _s in range(1, s+1):
        for _t in range(1, t+1):
            sys_rank = list(df[(df['sessions'] == _s) & (df['trial'] == _t)].sort_values(by='loglikelihood', ascending=False)['system'])
            corr, _ = kendalltau(ref, sys_rank)
            df_data.append({
                'queries': k,
                'sessions': _s,
                'trial': _t,
                'ktau': corr
            })
_df = pd.DataFrame(df_data)
sns.heatmap(_df.groupby(['queries', 'sessions']).mean().reset_index().pivot("queries", "sessions", "ktau"),
            square=True,
            cmap="Greens",
            ax=axes[0,0],
            cbar=False, 
            vmin=.0, 
            vmax=1.0)
axes[0,0].set_ylabel('DCM \n Number of Queries')
axes[0,0].set_title('LRM')
axes[0,0].tick_params(axis='both', which='both', length=0)
plt.setp(axes[0,0].get_xticklabels(), visible=False)
plt.setp(axes[0,0].get_yticklabels(), visible=False)
axes[0,0].set_xlabel('')

df_data = []
ref = [.4, .45, .5, .55, .6,  .65,  .7, .75, .8, .85, .9, .95, 1]
for k in [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,50]:
    df = pd.read_csv('experimental_results/' + model_name + '.ll.irm.' + str(k) + '.csv')
    s = 20
    t = 10
    for _s in range(1, s+1):
        for _t in range(1, t+1):
            sys_rank = list(df[(df['sessions'] == _s) & (df['trial'] == _t)].sort_values(by='loglikelihood', ascending=False)['weight'])
            corr, _ = kendalltau(ref, sys_rank)
            df_data.append({
                'queries': k,
                'sessions': _s,
                'trial': _t,
                'ktau': corr
            })
_df = pd.DataFrame(df_data)
sns.heatmap(_df.groupby(['queries', 'sessions']).mean().reset_index().pivot("queries", "sessions", "ktau"),
            square=True,
            cmap="Greens",
            ax=axes[0,1], 
            cbar=False, 
            vmin=.0, 
            vmax=1.0)
axes[0,1].set_ylabel('')
axes[0,1].set_title('IRM')
axes[0,1].tick_params(axis='both', which='both', length=0)
plt.setp(axes[0,1].get_xticklabels(), visible=False)
plt.setp(axes[0,1].get_yticklabels(), visible=False)
axes[0,1].set_xlabel('')

model_name = 'sdbn'

df_data = []
ref = ['XSqrA_M', 'BM25', 'Baseline', 'Tf', 'Dl', 'Null']
for k in [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,50]:

    df = pd.read_csv('experimental_results/' + model_name + '.ll.lrm.' + str(k) + '.csv')
    s = 20
    t = 10
    for _s in range(1, s+1):
        for _t in range(1, t+1):
            sys_rank = list(df[(df['sessions'] == _s) & (df['trial'] == _t)].sort_values(by='loglikelihood', ascending=False)['system'])
            corr, _ = kendalltau(ref, sys_rank)
            df_data.append({
                'queries': k,
                'sessions': _s,
                'trial': _t,
                'ktau': corr
            })
_df = pd.DataFrame(df_data)
sns.heatmap(_df.groupby(['queries', 'sessions']).mean().reset_index().pivot("queries", "sessions", "ktau"),
            square=True,
            cmap="Greens",
            ax=axes[1,0],
            cbar=False, 
            vmin=.0, 
            vmax=1.0)
axes[1,0].set_ylabel('SDBN \n Number of Queries')
axes[1,0].tick_params(axis='both', which='both', length=0)
plt.setp(axes[1,0].get_xticklabels(), visible=False)
plt.setp(axes[1,0].get_yticklabels(), visible=False)
axes[1,0].set_xlabel('Number of Sessions')

df_data = []
ref = [.4, .45, .5, .55, .6,  .65,  .7, .75, .8, .85, .9, .95, 1]
for k in [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,50]:
    df = pd.read_csv('experimental_results/' + model_name + '.ll.irm.' + str(k) + '.csv')
    s = 20
    t = 10
    for _s in range(1, s+1):
        for _t in range(1, t+1):
            sys_rank = list(df[(df['sessions'] == _s) & (df['trial'] == _t)].sort_values(by='loglikelihood', ascending=False)['weight'])
            corr, _ = kendalltau(ref, sys_rank)
            df_data.append({
                'queries': k,
                'sessions': _s,
                'trial': _t,
                'ktau': corr
            })
_df = pd.DataFrame(df_data)
sns.heatmap(_df.groupby(['queries', 'sessions']).mean().reset_index().pivot("queries", "sessions", "ktau"),
            square=True,
            cmap="Greens",
            ax=axes[1,1], 
            cbar=False, 
            vmin=.0, 
            vmax=1.0)
axes[1,1].set_ylabel('')
axes[1,1].tick_params(axis='both', which='both', length=0)
plt.setp(axes[1,1].get_xticklabels(), visible=False)
plt.setp(axes[1,1].get_yticklabels(), visible=False)
axes[1,1].set_xlabel('Number of Sessions')

plt.savefig('experimental_results/figures/dcm.sdbn.ktau.ll.heatmaps.pdf', format='pdf', bbox_inches='tight')
