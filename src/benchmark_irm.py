import pandas as pd
import pyterrier as pt
pt.init()

# download tripjudge here: https://github.com/sophiaalthammer/tripjudge
qrels = pd.read_csv('./tripjudge/data/qrels_2class.txt', sep=' ', names=['qid', 'Q0', 'docno', 'label'])
qrels['qid'] = qrels['qid'].apply(str)
qrels['docno'] = qrels['docno'].apply(str)

dataset = pt.get_dataset('irds:tripclick/test/head')
index = pt.IndexFactory.of('./indices/tripclick/data.properties')

DFRee = pt.BatchRetrieve(index, wmodel="DFRee") >> pt.pipelines.PerQueryMaxMinScoreTransformer()
Dl = pt.BatchRetrieve(index, wmodel="Dl") >> pt.pipelines.PerQueryMaxMinScoreTransformer()

alphas = [.4, .45, .5, .55, .6, .65, .7, .75, .8, .85, .9, .95, 1]

systems = [
    (1 - alpha)* DFRee + alpha * Dl for alpha in alphas
]

exp_res = pt.Experiment(
    systems,
    dataset.get_topics(),
    qrels,
    eval_metrics=['P_20', 'ndcg_cut_20', 'map'],
    names = [str(alpha) for alpha in alphas]
)

exp_res.to_csv('./experimental_results/benchmark.irm.tripjudge.2.grade.csv', index=False)
print(exp_res.to_markdown(tablefmt="grid", floatfmt="0.4f"))

