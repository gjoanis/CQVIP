"""
Document Chunker

Splits long regulatory documents into smaller searchable chunks.
"""


class DocumentChunker:
    """
    Splits document text into overlapping chunks for retrieval.
    """

    def __init__(self, chunk_size: int = 1200, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_document(self, document: dict):
        """
        Split one document into chunks.

        Args:
            document (dict): Source document with source, path, and text.

        Returns:
            list[dict]: Chunk records with text and metadata.
        """
        text = document.get("text", "")
        source = document.get("source", "unknown")
        path = document.get("path", "")

        chunks = []

        if not text.strip():
            return chunks

        start = 0
        chunk_id = 1

        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "chunk_id": f"{source}::chunk_{chunk_id}",
                        "source": source,
                        "path": path,
                        "text": chunk_text,
                    }
                )

            start += self.chunk_size - self.overlap
            chunk_id += 1

        return chunks

    def chunk_documents(self, documents: list[dict]):
        """
        Split multiple documents into chunks.
        """
        all_chunks = []

        for document in documents:
            all_chunks.extend(self.chunk_document(document))

        return all_chunks