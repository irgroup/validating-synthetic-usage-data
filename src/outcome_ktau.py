from scipy.stats import kendalltau

import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 

df_data = []

sns.set_theme()

ref = [.4, .45, .5, .55, .6,  .65,  .75, .8, .85, .9, .95, 1]

# for k in [25, 50]:
for k in [50]:
    for model_name in ['dctr', 'sdbn','dcm']:
        # model_name = 'sdbn'
        
        df = pd.read_csv('experimental_results/' + model_name + '.outcome.irm.' + str(k) + '.csv')
        df = df[df['weight'] != 0.7]
        s = 100
        t = 10
        for _s in range(10, s+1, 10):
            for _t in range(1, t+1):
                sys_rank = list(df[(df['sessions'] == _s) & (df['trial'] == _t)].sort_values(by='outcome', ascending=False)['weight'])
                corr, _ = kendalltau(ref, sys_rank)
                df_data.append({
                    # 'Click model': model_name.upper() + '; IRM; ' + str(k),
                    'Click model': model_name.upper() + '$\mathregular{_{IRM}}$',
                    'Sessions': _s,
                    'trial': _t,
                    'ktau': corr
                })
    
ref = ['XSqrA_M', 'BM25', 'Tf', 'Dl', 'Null']
# for k in [25, 50]:         
for k in [50]:         
    for model_name in ['dctr', 'sdbn','dcm']:
        # model_name = 'sdbn'
        # k = 50
        df = pd.read_csv('experimental_results/' + model_name + '.outcome.lrm.' + str(k) + '.csv')
        df = df[df['system'] != 'Baseline']
        s = 100
        t = 10
        for _s in range(10, s+1, 10):
            for _t in range(1, t+1):
                sys_rank = list(df[(df['sessions'] == _s) & (df['trial'] == _t)].sort_values(by='outcome', ascending=False)['system'])
                corr, _ = kendalltau(ref, sys_rank)
                df_data.append({
                    # 'Click model': model_name.upper() + '; LRM; ' + str(k),
                    'Click model': model_name.upper() + '$\mathregular{_{LRM}}$',
                    'Sessions': _s,
                    'trial': _t,
                    'ktau': corr
                })                
        
_df = pd.DataFrame(df_data)
f, ax = plt.subplots(figsize=(3,3))
sns.heatmap(_df.groupby(['Click model', 'Sessions']).mean().reset_index().pivot("Click model", "Sessions", "ktau"),
            square=False,
            cmap="Greens")
plt.title("Kendall's " + r"$\tau$")
plt.yticks(rotation=0) 
plt.yticks(fontsize=14)
ax.set(ylabel=None)
ax.set(xlabel='Number of Sessions')
# plt.show()
plt.savefig('experimental_results/figures/ktau.outcome.heatmaps.pdf', format='pdf', bbox_inches='tight')
