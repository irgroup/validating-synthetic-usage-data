import pyterrier as pt
pt.init()

dataset = pt.get_dataset('irds:tripclick')
indexer = pt.IterDictIndexer('./indices/tripclick', threads=6)
