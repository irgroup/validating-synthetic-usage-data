import pandas as pd
import pyterrier as pt
pt.init() 

# download tripjudge here: https://github.com/sophiaalthammer/tripjudge
qrels = pd.read_csv('./tripjudge/data/qrels_2class.txt', sep=' ', names=['qid', 'Q0', 'docno', 'label'])
qrels['qid'] = qrels['qid'].apply(str)
qrels['docno'] = qrels['docno'].apply(str)

dataset = pt.get_dataset('irds:tripclick/test/head')
index = pt.IndexFactory.of('./indices/tripclick/data.properties')

XSqrA_M = pt.BatchRetrieve(index, wmodel="XSqrA_M") 
BM25 = pt.BatchRetrieve(index, wmodel="BM25") 
Tf = pt.BatchRetrieve(index, wmodel="Tf")  
Dl = pt.BatchRetrieve(index, wmodel="Dl") 
null = pt.BatchRetrieve(index, wmodel="Null") 

dfree = pt.BatchRetrieve(index, wmodel="DFRee") >> pt.pipelines.PerQueryMaxMinScoreTransformer()
dl = pt.BatchRetrieve(index, wmodel="Dl") >> pt.pipelines.PerQueryMaxMinScoreTransformer()
alpha = 0.7
base = (1.0 - alpha) * dfree + alpha * dl

systems = [
    XSqrA_M,
    BM25,
    base,
    Tf,
    Dl, 
    null, 
]

exp_res = pt.Experiment(
    systems,
    dataset.get_topics(),
    qrels,
    eval_metrics=[
        'P_20', 
        'ndcg_cut_20', 
        'map'
        ],
    names=[
        "X^2",
        "BM25",
        "Baseline",
        "Tf",
        "Dl",
        "Null"
        ]
)

exp_res.to_csv('./experimental_results/benchmark.lrm.tripjudge.2.grade.csv', index=False)
print(exp_res.to_markdown(tablefmt="grid", floatfmt="0.4f"))
