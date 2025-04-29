import pandas as pd
import pyterrier as pt

from pyterrier_adaptive import CorpusGraph


class FFAdaptive(pt.Transformer):
    def __init__(
        self,
        corpus_graph: CorpusGraph,
        retriever: pt.terrier.Retriever,
        k: int,
    ):
        self.corpus_graph = corpus_graph
        self.retriever = retriever
        self.k = k
        super().__init__()

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        nb_df = self._append_neighbours(df)
        nb_df = self.retriever.transform(nb_df)
        return nb_df

    def _append_neighbours(self, df: pd.DataFrame) -> pd.DataFrame:
        corpus_graph = self.corpus_graph.to_limit_k(self.k)
        df = df.drop(columns=["docno", "rank", "score"])
        df["docid"] = df["docid"].apply(
            lambda docid: [docid] + [int(n) for n in corpus_graph.neighbours(docid)]
        )
        df = df.explode("docid", ignore_index=True)
        df = df.drop_duplicates(subset=["qid", "docid"], keep="first")

        return df

    def __repr__(self) -> str:
        return "fast_forward_ar"
