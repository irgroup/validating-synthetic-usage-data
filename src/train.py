import os
import random 
import pandas as pd
from util import database_collection, parse_session

from pyclick.click_models.CTR import DCTR
from pyclick.click_models.DCM import DCM
from pyclick.click_models.SDBN import SDBN

from pyclick.utils.Utils import Utils
from pyclick.click_models.task_centric.TaskCentricSearchSession import TaskCentricSearchSession
from pyclick.search_session.SearchResult import SearchResult
from pyclick.click_models.ParamContainer import RankParamContainer, RankPrevClickParamContainer
RankParamContainer.MAX_RANK_DEFAULT = 20
RankPrevClickParamContainer.MAX_RANK_DEFAULT = 20

queries = pd.read_csv('./experimental_results/train.head.50.csv')
dbc = database_collection()

cm = 'dctr'
m = 100 # samples 
n = 1 # trials

for _m in range(1, m+1):
    for _n in range(1, n+1):
        search_sessions = []
        for q in queries['query']:
            
            pipeline = [

                {'$match': {'Keywords' : q}},

                {"$group": 
                    {'_id': '$SessionId', 
                    'count': {'$sum': 1}, 
                    'clicks': {'$push': 
                        {'click': '$DocumentId', 
                        'documents': '$Documents', 
                        'query': '$Keywords'}
                        }
                    }
                }
                
            ]
            
            sessions = list(dbc.aggregate(pipeline))
            random.shuffle(sessions)

            cnt = 0
            for session in sessions:
                if cnt < _m:
                    _s = parse_session(session)
                    search_sessions.append(_s)
                    cnt += 1 
                else:
                    break
        
        click_model = globals()[cm.upper()]()
        click_model.train(search_sessions)
        
        f_name = '.'.join([cm, str(_m), str(_n), 'json'])
        
        path_out = os.path.join('experimental_results', cm, f_name)
        
        with open(path_out, 'w') as f_out:
            f_out.write(click_model.to_json())
