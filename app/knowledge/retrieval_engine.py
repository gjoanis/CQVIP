"""
CQVIP Retrieval Engine

Retrieves the most relevant regulatory document chunks
from the vector store.
"""

from .embedding_service import EmbeddingService
from .vector_store import VectorStore


class RetrievalEngine:
    """
    Performs semantic search against the regulatory knowledge base.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def retrieve(self, query: str, top_k: int = 5):
        """
        Retrieve the most relevant document chunks.

        Args:
            query (str): User question or requirement.
            top_k (int): Number of chunks to return.

        Returns:
            dict: Raw ChromaDB search results.
        """

        query_embedding = self.embedding_service.embed_text(query)

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        return results