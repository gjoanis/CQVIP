"""
Embedding Service

Creates vector embeddings for regulatory document chunks.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

class EmbeddingService:
    """
    Uses OpenAI embeddings to convert text into vectors.
    """

    def __init__(self, model: str = "text-embedding-3-small"):
        load_dotenv()
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def embed_text(self, text: str):
        """
        Create an embedding for a single text string.
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding

    def embed_chunks(self, chunks: list[dict]):
        """
        Add embeddings to document chunks.
        """
        embedded_chunks = []

        for chunk in chunks:
            embedding = self.embed_text(chunk["text"])

            embedded_chunks.append(
                {
                    **chunk,
                    "embedding": embedding,
                }
            )

        return embedded_chunks