import math
import pandas as pd
import pyterrier as pt

from pyclick.click_models.CTR import DCTR
from pyclick.click_models.DCM import DCM
from pyclick.click_models.SDBN import SDBN

from pyclick.utils.Utils import Utils
from pyclick.click_models.task_centric.TaskCentricSearchSession import TaskCentricSearchSession
from pyclick.search_session.SearchResult import SearchResult
from pyclick.click_models.ParamContainer import RankParamContainer, RankPrevClickParamContainer
RankParamContainer.MAX_RANK_DEFAULT = 20
RankPrevClickParamContainer.MAX_RANK_DEFAULT = 20

queries = pd.read_csv('experimental_results/train.head.50.csv')
queries = queries.replace(to_replace=r'\w+:\w+', value='', regex=True)
k = 50
queries = queries.iloc[:k]

pt.init(boot_packages=["com.github.terrierteam:terrier-prf:-SNAPSHOT"])
index = pt.IndexFactory.of('./indices/tripclick/data.properties')

_qrels = pt.get_dataset('irds:tripclick/train/head/dctr').get_qrels()

qrels = {}
for qid in queries['qid']:
    for entry in _qrels[_qrels['qid'] == str(qid)].iterrows():
        qrels[(entry[1].qid, entry[1].docno)] = entry[1].label

model_name = 'dctr'    

data = []

DFRee = pt.BatchRetrieve(index, wmodel="DFRee") >> pt.pipelines.PerQueryMaxMinScoreTransformer()
Dl = pt.BatchRetrieve(index, wmodel="Dl") >> pt.pipelines.PerQueryMaxMinScoreTransformer()

weights = [.4, .45, .5, .55, .6,  .65,  .7, .75, .8, .85, .9, .95, 1]

for w in weights:

    if w == 0.0:
        method = pt.BatchRetrieve(index, wmodel="DFRee")
    else:
        method = (1 - w)* DFRee + w * Dl 

    lls = []
    
    for samples in range(1, 101):
        for t in range(1, 11):
            click_model = DCTR()
            with open('experimental_results/' + model_name + '/' + model_name  + '.' + str(samples) + '.' + str(t) + '.json', 'r') as f_in:
                json_str = f_in.read()
                click_model.from_json(json_str)
                
            probs = []

            for query in queries['query']:
                res = method.search(query)

                _session = TaskCentricSearchSession('0', query)
                for result in list(res[:20]['docno']):
                    _result = SearchResult(result, 0)
                    _session.web_results.append(_result)
                _probs = click_model.get_conditional_click_probs(_session)   
                probs.append(_probs)              

            loglikelihood = 0

            for _probs in probs:
                log_click_probs = [math.log(prob) for prob in _probs]
                if len(log_click_probs) > 0:
                    loglikelihood += sum(log_click_probs) / len(log_click_probs)

            loglikelihood /= len(probs)
            print("Queries:", str(k), "\tWeight:", str(w), "\tSessions:", str(samples),"\tTrial:", str(t) ,"\tLogLikelihood:", loglikelihood) 
            data.append({
                'loglikelihood': loglikelihood,
                'weight': w,
                'sessions': samples,
                'trial': t
            })

pd.DataFrame(data).to_csv('experimental_results/' + model_name + '.ll.irm.' + str(k) + '.csv', index=False)

################################################################################
#### plot dctr by loglikelihood on dfree and dl interpolation ##################

# import pandas as pd 
# import matplotlib.pyplot as plt
# import seaborn as sns 

# sns.set_theme()
# k = 50
# model_name = 'dctr'
# df = pd.read_csv('experimental_results/' + model_name + '.ll.irm.' + str(k) + '.csv')

# df = df[df['weight'] != 0.0]

# plt.figure(figsize = (5,5))
# sns.lineplot(x="sessions", y="loglikelihood",
#              hue="weight",
#              data=df)
# plt.title(str(k) + ' queries')
# plt.legend(bbox_to_anchor=(1,1), loc="upper left")
# plt.savefig('experimental_results/figures/' + model_name + '.ll.irm.' + str(k) + '.pdf', format='pdf', bbox_inches='tight')

################################################################################
##### plot heatmap kendall's tau interpolations dfree+dl #######################

# from scipy.stats import kendalltau

# import pandas as pd 
# import matplotlib.pyplot as plt
# import seaborn as sns 

# df_data = []

# sns.set_theme(style="white")

# ref = [.4, .45, .5, .55, .6,  .65,  .7, .75, .8, .85, .9, .95, 1]

# for k in [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,50]:
#     model_name = 'dctr'
#     df = pd.read_csv('experimental_results/' + model_name + '.ll.irm.' + str(k) + '.csv')
#     s = 20
#     t = 10
#     for _s in range(1, s+1):
#         for _t in range(1, t+1):
#             sys_rank = list(df[(df['sessions'] == _s) & (df['trial'] == _t)].sort_values(by='loglikelihood', ascending=False)['weight'])
#             corr, _ = kendalltau(ref, sys_rank)
#             df_data.append({
#                 'queries': k,
#                 'sessions': _s,
#                 'trial': _t,
#                 'ktau': corr
#             })

# #### heatmap
# _df = pd.DataFrame(df_data)
# f, ax = plt.subplots(figsize=(9,9))
# sns.heatmap(_df.groupby(['queries', 'sessions']).mean().reset_index().pivot("queries", "sessions", "ktau"),
#             square=True,
#             cmap="Greens")
# plt.savefig('experimental_results/figures/' + model_name + '.ktau.ll.heatmap.irm.pdf', format='pdf', bbox_inches='tight')