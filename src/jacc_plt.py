import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10,2))

df = pd.read_csv('experimental_results/jacc.lrm.csv', index_col=0)
df = df.drop('Baseline').drop(columns='Baseline')
df.rename(columns = {'XSqrA_M' : 'DFR $\chi^2$'}, inplace = True)
df.rename({'XSqrA_M' : 'DFR $\chi^2$'}, inplace = True)
mask = np.triu(np.ones_like(df))
sns.heatmap(df, mask=mask, vmin=0, vmax=0.5, ax=axes[0], cbar=False,)
for tick in axes[0].get_yticklabels():
    tick.set_rotation(0)

df = pd.read_csv('experimental_results/jacc.irm.csv', index_col=0)
mask = np.triu(np.ones_like(df))
sns.heatmap(df, mask=mask, vmin=0, vmax=0.5, ax=axes[1])
for tick in axes[1].get_yticklabels():
    tick.set_rotation(0)
    
plt.suptitle('Jaccard similarity between the first 20 results')
plt.savefig('experimental_results/figures/jacc_sim.pdf', format='pdf', bbox_inches='tight')
