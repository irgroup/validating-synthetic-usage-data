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

systems = [
    'XSqrA_M',
    'BM25',
    'Baseline',
    'Tf',
    'Dl', 
    'Null', 
]
    
for t in range(1,11):
    
    for s in systems:
        
        if s == 'Baseline':
            dfree = pt.BatchRetrieve(index, wmodel="DFRee") >> pt.pipelines.PerQueryMaxMinScoreTransformer()
            dl = pt.BatchRetrieve(index, wmodel="Dl") >> pt.pipelines.PerQueryMaxMinScoreTransformer()
            alpha = 0.7
            method = (1.0 - alpha) * dfree + alpha * dl
        else:
            method = pt.BatchRetrieve(index, wmodel=s) 

        lls = []

        for samples in range(1, 101):

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
            print("Queries:", str(k), "\tSystem:", str(s), "\tSessions:", str(samples),"\tTrial:", str(t) ,"\tLogLikelihood:", loglikelihood) 
            data.append({
                'loglikelihood': loglikelihood,
                'system': s,
                'sessions': samples,
                'trial': t
            })

pd.DataFrame(data).to_csv('experimental_results/' + model_name + '.ll.lrm.' + str(k) + '.csv', index=False)

################################################################################
#### plot dctr by loglikelihood on experimental systems ########################

# import pandas as pd 
# import matplotlib.pyplot as plt
# import seaborn as sns 

# sns.set_theme()
# k = 50
# model_name = 'sdbn'
# df = pd.read_csv('experimental_results/' + model_name + '.ll.lrm.' + str(k) + '.csv')

# df = df[df['system'] != 'LemurTF_IDF']

# plt.figure(figsize = (5,5))
# sns.lineplot(x="sessions", y="loglikelihood",
#             hue="system",
#             data=df)
# plt.title(str(k) + ' queries')
# plt.legend(bbox_to_anchor=(1,1), loc="upper left")
# plt.savefig('experimental_results/figures/' + model_name + '.ll.lrm.' + str(k) + '.pdf', format='pdf', bbox_inches='tight')

################################################################################
#### plot heatmap kendall's tau experimental systems ###########################

# from scipy.stats import kendalltau

# import pandas as pd 
# import matplotlib.pyplot as plt
# import seaborn as sns 

# df_data = []

# sns.set_theme()

# ref = ['XSqrA_M', 'BM25', 'Baseline', 'Tf', 'Dl', 'Null']

# for k in [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,50]:
#     model_name = 'dctr'
#     df = pd.read_csv('experimental_results/' + model_name + '.ll.lrm.' + str(k) + '.csv')
#     df = df[df['system'] != 'LemurTF_IDF']
#     s = 20
#     t = 10
#     for _s in range(1, s+1):
#         for _t in range(1, t+1):
#             sys_rank = list(df[(df['sessions'] == _s) & (df['trial'] == _t)].sort_values(by='loglikelihood', ascending=False)['system'])
#             corr, _ = kendalltau(ref, sys_rank)
#             df_data.append({
#                 'queries': k,
#                 'sessions': _s,
#                 'trial': _t,
#                 'ktau': corr
#             })

# _df = pd.DataFrame(df_data)
# f, ax = plt.subplots(figsize=(9,9))
# sns.heatmap(_df.groupby(['queries', 'sessions']).mean().reset_index().pivot("queries", "sessions", "ktau"),
#             square=True,
#             cmap="Greens")
# plt.title("Kendall's tau")
# plt.yticks(rotation=0) 
# plt.savefig('experimental_results/figures/' + model_name + '.ktau.ll.heatmap.lrm.pdf', format='pdf', bbox_inches='tight')
