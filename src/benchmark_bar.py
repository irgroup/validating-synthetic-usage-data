import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")


fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(10,2))

df = pd.read_csv('./experimental_results/benchmark.lrm.tripjudge.2.grade.csv')

_p20 = df[df['name'] == 'Baseline']['P_20'].iloc[0]
_ndcg20 = df[df['name'] == 'Baseline']['ndcg_cut_20'].iloc[0]
_map = df[df['name'] == 'Baseline']['map'].iloc[0]

df = df[df['name'] != 'Baseline']
df = df.replace('Baseline', 'Base')
df = df.replace('X^2', 'DFR $\chi^2$')
df.sort_values(by='P_20', ascending=False).plot.bar(x='name', ax=axes[0])
plt.ylabel('Score')
axes[0].set_xlabel('System')
axes[0].legend(['P@20', 'nDCG@20', 'AP'])
axes[0].axhline(_p20, ls='--', color='tab:blue')
axes[0].axhline(_ndcg20, ls='--', color='tab:orange')
axes[0].axhline(_map, ls='--', color='tab:green')

df = pd.read_csv('./experimental_results/benchmark.irm.tripjudge.2.grade.csv')
df = df[df['name'] != 0.7]
df.sort_values(by='ndcg_cut_20', ascending=False).plot.bar(x='name', ax=axes[1])
plt.ylabel('Score')
axes[1].set_xlabel(r'$\alpha$')
axes[1].legend(['P@20', 'nDCG@20', 'AP'])
axes[1].axhline(_p20, ls='--', color='tab:blue')
axes[1].axhline(_ndcg20, ls='--', color='tab:orange')
axes[1].axhline(_map, ls='--', color='tab:green')

plt.suptitle('External validation with editorial relevance labels')
plt.savefig('./experimental_results/figures/benchmarks.tripjudge.pdf', type='pdf', format='pdf', bbox_inches='tight')
