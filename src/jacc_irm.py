import pandas as pd
import pyterrier as pt
pt.init()

def jaccard(ref,exp):
    overlap = ref & exp
    union = ref.union(exp)
    return len(overlap) / len(union)

df = pd.read_csv('ignore/head-train-50.csv')
df = df.replace(to_replace=r'\w+:\w+', value='', regex=True)

dataset = pt.get_dataset('irds:tripclick/val/head/dctr')
index = pt.IndexFactory.of('./indices/tripclick/data.properties')

dfree = pt.BatchRetrieve(index, wmodel="DFRee") >> pt.pipelines.PerQueryMaxMinScoreTransformer()
dl = pt.BatchRetrieve(index, wmodel="Dl") >> pt.pipelines.PerQueryMaxMinScoreTransformer()

alphas = [.4, .45, .5, .55, .6,  .65,  .7, .75, .8, .85, .9, .95, 1]

df_data = {}

for _ref in alphas:
    
    _data = {}
    
    for _exp in alphas:
        ref = (1.0 - _ref) * dfree + _ref * dl
        exp = (1.0 - _exp) * dfree + _exp * dl

        j = []

        for row in df.iterrows():
            query = row[1].query

            ref_docs = set(ref.search(query).iloc[:20]['docid'])
            exp_docs = set(exp.search(query).iloc[:20]['docid'])

            j.append(jaccard(ref_docs,exp_docs))
                        
        _data[_exp] = sum(j) / len(j)   
    
    df_data[_ref] = _data
    
pd.DataFrame.from_dict(df_data).to_csv('experimental_results/jacc.irm.csv')
