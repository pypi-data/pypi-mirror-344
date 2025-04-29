# FFAR
Adaptive Retrieval component for Efficient Retrieval

## Installation
Install the package via `pip`:
```bash
pip install ff-adaptive
```
## Getting Started
1. Create an [Index](https://pyterrier.readthedocs.io/en/latest/terrier-indexing.html)
2. Run the following code:
```bash
import pyterrier as pt
from pyterrier_adaptive import CorpusGraph
from pyterrier_pisa import PisaIndex

from ff_adaptive import FFAdaptive

if __name__ == "__main__":
    corpus_graph = CorpusGraph.from_hf("macavaney/msmarco-passage.corpusgraph.bm25.128")
    dataset = pt.get_dataset(f"irds:msmarco-passage/trec-dl-2019/judged")
    index = pt.IndexFactory.of("/path/to/your/index") # Replace with index path
    bm25 = pt.terrier.Retriever(index, wmodel="BM25")

    rerank_model = pt.terrier.Retriever(index, wmodel="BM25") # Replace with a re-ranker of choice

    pipeline = bm25 >> FFAdaptive(corpus_graph=corpus_graph, retriever=bm25, k=16) >> rerank_model

    result = pipeline.transform(dataset.get_topics())
    print(result)
```

## Citation
```bibtex
@inproceedings{rear2025,
    title = {Resource Efficient Adaptive Retrieval},
    author = {Martijn Smits},
    year = {2025},
}
```