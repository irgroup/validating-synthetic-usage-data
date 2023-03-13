import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 

sns.set_theme()
fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(15,4))

df_data = []

cm = ['dctr', 'dcm', 'sdbn']

for model_name in cm:
    k = 50
    df = pd.read_csv('experimental_results/' + model_name + '.outcome.lrm.' + str(k) + '.csv')
    df = df[df['system'] != 'Baseline']
    _s = 100
    t = 10
    for _t in range(1, t+1):
        for row in df[(df['sessions'] == _s) & (df['trial'] == _t)].iterrows():
            df_data.append({
                'cm': model_name,
                'system': row[1].system,
                'trial': _t,
                'outcome': row[1].outcome
            })

_df = pd.DataFrame(df_data)
ax = sns.barplot(x="system", y="outcome", hue="cm", data=_df, capsize=.1, ax=axes[0])
ax.axhline(0.5, ls='--', color='grey')

df_data = []

for model_name in cm:
    k = 50
    df = pd.read_csv('experimental_results/' + model_name + '.outcome.irm.' + str(k) + '.csv')
    df = df[df['weight'] != 0.7]
    _s = 100
    t = 10
    for _t in range(1, t+1):
        
        for row in df[(df['sessions'] == _s) & (df['trial'] == _t)].iterrows():
            df_data.append({
                'cm': model_name,
                'weight': row[1].weight,
                'trial': _t,
                'outcome': row[1].outcome
            })

_df = pd.DataFrame(df_data)
ax = sns.barplot(x="weight", y="outcome", hue="cm", data=_df, capsize=.1, ax=axes[1])
ax.axhline(0.5, ls='--', color='grey')
plt.savefig('experimental_results/figures/bar.plots.outcome.50.pdf', format='pdf', bbox_inches='tight')
