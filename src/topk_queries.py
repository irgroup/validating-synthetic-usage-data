from util import database_collection
import ir_datasets
import pandas as pd

k = 50

dbc = database_collection()

data = []

dataset = ir_datasets.load("tripclick/train/head")
for query in dataset.queries_iter():
    results = dbc.find({"Keywords": query.text})
    # print(query.text, len(list(results)))
    data.append({
        'qid': query.query_id,
        'query': query.text,
        'cnt': len(list(results))
    })
    
df = pd.DataFrame(data)
df = df.replace(to_replace=r'\w+:\w+', value='', regex=True)
df = df.sort_values(by='cnt', ascending=False)
# df.to_csv('./experimental_results/head.csv', index=False)

file_name = '.'.join(['train', 'head', str(k)])
df.iloc[:k].to_csv('./experimental_results/' + file_name + '.csv', index=False)
