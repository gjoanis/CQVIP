"""
CQVIP Document Indexer

Coordinates the full indexing pipeline:
load documents, chunk text, create embeddings, and store chunks.
"""

from .regulatory_loader import RegulatoryLoader
from .chunker import DocumentChunker
from .embedding_service import EmbeddingService
from .vector_store import VectorStore


class DocumentIndexer:
    """
    Indexes regulatory documents into the CQVIP Knowledge Engine.
    """

    def __init__(self):
        self.loader = RegulatoryLoader()
        self.chunker = DocumentChunker()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def index_regulatory_documents(self, force_reindex: bool = False):
        """
        Run the complete indexing pipeline.

        If the vector store already has records, skip indexing unless force_reindex=True.
        """

        existing_count = self.vector_store.count()

        if existing_count > 0 and not force_reindex:
            return {
                "status": "skipped",
                "documents_loaded": 0,
                "chunks_indexed": existing_count,
                "message": "Knowledge base already indexed. Skipping re-index.",
            }

        documents = self.loader.load_documents()

        if not documents:
            return {
                "status": "empty",
                "documents_loaded": 0,
                "chunks_indexed": 0,
                "message": "No regulatory documents found.",
            }

        chunks = self.chunker.chunk_documents(documents)

        if not chunks:
            return {
                "status": "empty",
                "documents_loaded": len(documents),
                "chunks_indexed": 0,
                "message": "Documents loaded, but no chunks were created.",
            }

        self.vector_store.reset()

        embedded_chunks = self.embedding_service.embed_chunks(chunks)

        self.vector_store.add_chunks(embedded_chunks)

        return {
            "status": "success",
            "documents_loaded": len(documents),
            "chunks_indexed": len(embedded_chunks),
            "message": "Regulatory documents indexed successfully.",
        }