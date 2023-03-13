import pandas as pd
import pyterrier as pt
pt.init()

def jaccard(ref,exp):
    overlap = ref & exp
    union = ref.union(exp)
    return len(overlap) / len(union)

df = pd.read_csv('./experimental_results/train.head.50.csv')
df = df.replace(to_replace=r'\w+:\w+', value='', regex=True)

dataset = pt.get_dataset('irds:tripclick/val/head/dctr')
index = pt.IndexFactory.of('./indices/tripclick/data.properties')

systems = ['XSqrA_M', 'BM25', 'Baseline', 'Tf', 'Dl', 'Null']

df_data = {}

dfree = pt.BatchRetrieve(index, wmodel="DFRee") >> pt.pipelines.PerQueryMaxMinScoreTransformer()
dl = pt.BatchRetrieve(index, wmodel="Dl") >> pt.pipelines.PerQueryMaxMinScoreTransformer()

_alpha = 0.7

for _ref in systems:
    
    _data = {}
    
    for _exp in systems:
        if _ref == 'Baseline':
            ref = (1.0 - _alpha) * dfree + _alpha * dl
        else:
            ref = pt.BatchRetrieve(index , wmodel=_ref) # ['XSqrA_M', 'BM25', 'Tf', 'Dl', 'Null']
        if _exp == 'Baseline':
            exp = (1.0 - _alpha) * dfree + _alpha * dl
        else:
            exp = pt.BatchRetrieve(index , wmodel=_exp)
            
        j = []

        for row in df.iterrows():
            query = row[1].query

            ref_docs = set(ref.search(query).iloc[:20]['docid'])
            exp_docs = set(exp.search(query).iloc[:20]['docid'])

            j.append(jaccard(ref_docs,exp_docs))
                        
        _data[_exp] = sum(j) / len(j)   
    
    df_data[_ref] = _data
    
pd.DataFrame.from_dict(df_data).to_csv('experimental_results/jacc.lrm.csv')
