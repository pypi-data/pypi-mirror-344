from .interfaces import Retrieval
from sentence_transformers import CrossEncoder

class Reranker(Retrieval):
    def __init__(self,reranker_model: str = 'cross-encoder/ms-marco-TinyBERT-L2-v2'):

        self.reranker_model=None
        self.config(reranker_model)

    def config(
            self,
            reranker_model : str):
        self.reranker_model=CrossEncoder(reranker_model)
        
    def retrieve(self,user_query : str, results : list,top_k : int):

        """
        Apply the re-ranking logic to the retrieved results.
        :param query: The user query.
        :param results: The initial set of results to be re-ranked.
        :return: A list of re-ranked results.
        """
        
        pairs= [(user_query, doc) for doc in results]
        scores = self.reranker_model.predict(pairs)
        ranked_documents = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)
        sentences_only = [doc[0] for doc in ranked_documents[:top_k]]

        return sentences_only
        