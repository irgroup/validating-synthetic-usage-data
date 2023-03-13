from scipy.stats import kendalltau

import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 

df_data = []

sns.set_theme()
fig, axes = plt.subplots(nrows=1, ncols=2, sharey=False, figsize=(7,3))

ref = ['XSqrA_M', 'BM25', 'Tf', 'Dl', 'Null']

click_models = ['dctr', 'sdbn', 'dcm',]
for model_name in click_models:
    k = 50
    df = pd.read_csv('experimental_results/' + model_name + '.outcome.lrm.' + str(k) + '.csv')
    df = df[df['system'] != 'Baseline']
    s = 100
    t = 10
    for _s in range(1, s+1, 1):
        for _t in range(1, t+1):
            sys_rank = list(df[(df['sessions'] == _s) & (df['trial'] == _t)].sort_values(by='outcome', ascending=False)['system'])
            corr, _ = kendalltau(ref, sys_rank)
            df_data.append({
                'cm': model_name,
                'sessions': _s,
                'trial': _t,
                'ktau': corr
            })      
_df = pd.DataFrame(df_data)

_df['rel_err'] = 1 - _df.groupby(['cm', 'trial']).cumsum()['ktau'] / _df['sessions']

ax = sns.lineplot(x="sessions", y="rel_err",
                  hue="cm",
                  data=_df, 
                  err_style='band', 
                  ax=axes[0], 
                  ci=95
                  )
ax.set(xlabel='Number of sessions')
ax.set(ylabel=r'$\delta \tau$')

handles, labels = axes[0].get_legend_handles_labels()
axes[0].legend(handles=handles, labels=[l.upper() for l in labels])
axes[0].set_title('LRM')

ref = [.4, .45, .5, .55, .6, .65, .75, .8, .85, .9, .95, 1]
df_data = []
click_models = ['dctr', 'sdbn', 'dcm',]
for model_name in click_models:
    k = 50
    df = pd.read_csv('experimental_results/' + model_name + '.outcome.irm.' + str(k) + '.csv')
    df = df[df['weight'] != .7]
    s = 100
    t = 10
    for _s in range(1, s+1, 1):
        for _t in range(1, t+1):
            sys_rank = list(df[(df['sessions'] == _s) & (df['trial'] == _t)].sort_values(by='outcome', ascending=False)['weight'])
            corr, _ = kendalltau(ref, sys_rank)
            df_data.append({
                'cm': model_name,
                'sessions': _s,
                'trial': _t,
                'ktau': corr
            })
            
_df = pd.DataFrame(df_data)

# _df['rel_err'] = (_df['sessions'] - _df.groupby(['cm', 'trial']).cumsum()['ktau']) / _df['sessions']
_df['rel_err'] = 1 - _df.groupby(['cm', 'trial']).cumsum()['ktau'] / _df['sessions']
ax = sns.lineplot(x="sessions", y="rel_err",
            hue="cm",
            data=_df, 
            err_style='band', 
            ax=axes[1],
            ci=95
            )
# axes[1].get_legend().remove()
ax.set(xlabel='Number of sessions')
ax.set(ylabel=' ')

handles, labels = axes[1].get_legend_handles_labels()
axes[1].legend(handles=handles, labels=[l.upper() for l in labels])
axes[1].set_title('IRM')
# ax.legend(['DCTR', 'SDBN', 'DCM'])
# plt.show()
plt.savefig('experimental_results/figures/' + '.'.join(click_models) + '.rel.err.' + str(k) + '.pdf', format='pdf', bbox_inches='tight')
