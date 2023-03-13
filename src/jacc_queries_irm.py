import os
import pandas as pd
import pyterrier as pt
from scipy.stats import wilcoxon

from pyclick.click_models.CTR import DCTR
from pyclick.click_models.DCM import DCM
from pyclick.click_models.SDBN import SDBN

from pyclick.utils.Utils import Utils
from pyclick.click_models.task_centric.TaskCentricSearchSession import TaskCentricSearchSession
from pyclick.search_session.SearchResult import SearchResult
from pyclick.click_models.ParamContainer import RankParamContainer, RankPrevClickParamContainer
RankParamContainer.MAX_RANK_DEFAULT = 20
RankPrevClickParamContainer.MAX_RANK_DEFAULT = 20

from util import interleave

pt.init()

def jaccard(ref,exp):
    overlap = ref & exp
    union = ref.union(exp)
    return len(overlap) / len(union)

k = 50

queries = pd.read_csv('./experimental_results/train.head.50.csv')
queries = queries.replace(to_replace=r'\w+:\w+', value='', regex=True)
queries = queries.iloc[:k]

index = pt.IndexFactory.of('./indices/tripclick/data.properties')
qrels = pt.get_dataset('irds:tripclick/train/head/dctr').get_qrels()

d = {}

dfree = pt.BatchRetrieve(index, wmodel="DFRee") >> pt.pipelines.PerQueryMaxMinScoreTransformer()
dl = pt.BatchRetrieve(index, wmodel="Dl") >> pt.pipelines.PerQueryMaxMinScoreTransformer()
alpha = .7
base = (1.0 - alpha) * dfree + alpha * dl

weights = [.4, .45, .5, .55, .6,  .65, .75, .8, .85, .9, .95, 1]

cm = 'dctr'
click_model = globals()[cm.upper()]()

for sessions in range(100, 101):
    for trial in range(10, 11):

        # load click model
        f_name = '.'.join([cm, str(sessions), str(trial), 'json'])
        path_in = os.path.join('experimental_results', cm, f_name)
        with open(path_in, 'r') as f_in:
            json_str = f_in.read()
            click_model.from_json(json_str)
            
        # determine probabilites for unknown items to identify an indifferent click decision for ties
        _unk = TaskCentricSearchSession('0', queries['query'].iloc[0])
        for i in range(1,21):
            _result = SearchResult('.'.join(['UNK', str(i)]), 0)
            _unk.web_results.append(_result)
        _unk_probs = click_model.get_conditional_click_probs(_unk)

        for weight in weights:
        
            exp = (1 - weight)* dfree + weight * dl
        
            wins = 0
            ties = 0
            results = []
        
            tie_queries = []
            win_queries = []
            loss_queries = []
                                
            for query in queries['query']:

                res_base = base.search(query)
                res_exp = exp.search(query)
                tdi = interleave(list(res_base['docno']), list(res_exp['docno']))
        
                ## determine win by max criterion
                cnt = 0
                _session = TaskCentricSearchSession('0', query)
                
                for item in tdi.values():
                    if cnt < 20:
                        result = item.get('docid')
                        _result = SearchResult(result, 0)
                        _session.web_results.append(_result)
                        cnt += 1
                _probs = click_model.get_conditional_click_probs(_session)
                
                if _unk_probs == _probs:
                    ties += 1
                    results.append(0)
                    tie_queries.append(query)
                    continue
                    # print(query, ': tie')

                val = max(_probs)
                idx = _probs.index(val) + 1
                
                if tdi.get(idx).get('type') == 'EXP':
                    wins += 1
                    results.append(1)
                    win_queries.append(query)
                    # print(query, ': win')
                else:
                    results.append(-1)
                    loss_queries.append(query)
                    # print(query, ': loss')
                    
            # determine outcome according to wins / (wins + losses)
            outcome = wins / (len(queries['query']) - ties)
            
            w, p = wilcoxon(results, [1] * k)
       
            d[weight] = {'win': win_queries,
                         'loss': loss_queries,
                         'tie': tie_queries}
   
wins_data = {}
ties_data = {}
loss_data = {}
            
for w in weights:
    _jacc_wins = {}
    _jacc_ties = {}
    _jacc_loss = {}
    for _w in weights:
        _jacc_wins[_w] = jaccard(set(d[w]['win']), set(d[_w]['win']))
        _jacc_ties[_w] = jaccard(set(d[w]['tie']), set(d[_w]['tie']))
        _jacc_loss[_w] = jaccard(set(d[w]['loss']), set(d[_w]['loss']))
        
    wins_data[w] = _jacc_wins               
    ties_data[w] = _jacc_ties               
    loss_data[w] = _jacc_loss               
          
pd.DataFrame.from_dict(wins_data).to_csv('experimental_results/irm.queries.win.csv')
pd.DataFrame.from_dict(ties_data).to_csv('experimental_results/irm.queries.tie.csv')
pd.DataFrame.from_dict(loss_data).to_csv('experimental_results/irm.queries.loss.csv')

################################################################################
#### plot: jaccard similartity between winning and losing queries ##############          
            
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 
import numpy as np

sns.set_theme()            

fig, ax = plt.subplots(figsize=(7, 5))

df_win = pd.read_csv('experimental_results/irm.queries.win.csv',index_col=0)
df_loss = pd.read_csv('experimental_results/irm.queries.loss.csv',index_col=0)

mask_win = np.triu(np.ones_like(df_win))
mask_loss = np.tril(np.ones_like(df_loss))

sns.heatmap(df_win, square=True, mask=mask_win, cmap="Greens", ax=ax, vmin=0.0, vmax=1.0, cbar=False)
sns.heatmap(df_loss, square=True, mask=mask_loss, cmap="Greens", ax=ax, vmin=0.0, vmax=1.0)

ax.patch.set_facecolor('lightgrey')
ax.patch.set_edgecolor('green')
ax.patch.set_hatch('xx')

ax.set_xlabel(r'$\alpha$')
ax.set_ylabel(r'$\alpha$')
ax.set_title('Jaccard similarity')
plt.savefig('experimental_results/figures/jacc.sim.wins.losses.pdf', type='pdf', format='pdf', bbox_inches='tight')
plt.show() 
