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

k = 50 # k = 5, 10, 25, 50

queries = pd.read_csv('./experimental_results/train.head.50.csv')
queries = queries.replace(to_replace=r'\w+:\w+', value='', regex=True)
queries = queries.iloc[:k]

index = pt.IndexFactory.of('./indices/tripclick/data.properties')
qrels = pt.get_dataset('irds:tripclick/train/head/dctr').get_qrels()

df_data = []

dfree = pt.BatchRetrieve(index, wmodel="DFRee") >> pt.pipelines.PerQueryMaxMinScoreTransformer()
dl = pt.BatchRetrieve(index, wmodel="Dl") >> pt.pipelines.PerQueryMaxMinScoreTransformer()
alpha = .7
base = (1.0 - alpha) * dfree + alpha * dl

XSqrA_M = pt.BatchRetrieve(index, wmodel="XSqrA_M") 
BM25 = pt.BatchRetrieve(index, wmodel="BM25") 
LemurTF_IDF = pt.BatchRetrieve(index, wmodel="LemurTF_IDF") 
Tf = pt.BatchRetrieve(index, wmodel="Tf") 
Dl = pt.BatchRetrieve(index, wmodel="Dl") 
null = pt.BatchRetrieve(index, wmodel="Null") 

systems = ["XSqrA_M", "BM25", "Baseline", "Tf", "Dl", "Null"]

cm = 'dctr' # cm = 'dctr', 'cm', 'dcm', 'pbm', 'sdbn', 'ubm'
click_model = globals()[cm.upper()]()

for sessions in range(1, 101):
    for trial in range(1, 11):

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

        for system in systems:
            if system == 'Baseline':
                exp = base
            else:
                exp = pt.BatchRetrieve(index, wmodel=system)
        
            wins = 0
            ties = 0
            results = []
                    
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
                    continue

                val = max(_probs)
                idx = _probs.index(val) + 1
                
                if tdi.get(idx).get('type') == 'EXP':
                    wins += 1
                    results.append(1)
                else:
                    results.append(-1)
        
            # determine outcome according to wins / (wins + losses)
            outcome = wins / (len(queries['query']) - ties)
            w, p = wilcoxon(results, [1] * k)
            
            df_data.append({'system': system,
                            'sessions': sessions,
                            'trial': trial,
                            'outcome': outcome,
                            'p_val': p})
            
            print("Queries:", str(k), "\tClick model:", cm, "\tSystem:", str(system), "\tSessions:", str(sessions),"\tTrial:", str(trial) ,"\tOutcome:", outcome ,"\tWilcoxon (p-val):", p)  

f_out_name = cm + '.outcome.lrm.' + str(k) + '.csv'

pd.DataFrame(df_data).to_csv('experimental_results/' + f_out_name, index=False)
