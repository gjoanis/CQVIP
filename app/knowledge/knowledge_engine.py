"""
CQVIP Knowledge Engine

Public interface for the CQVIP Retrieval-Augmented Generation (RAG) system.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

from .document_indexer import DocumentIndexer
from .retrieval_engine import RetrievalEngine
from .citation_engine import CitationEngine


class KnowledgeEngine:
    """
    Main interface to the CQVIP Knowledge Engine.
    """

    def __init__(self):
        self.indexer = DocumentIndexer()
        self.retriever = RetrievalEngine()
        self.citation_engine = CitationEngine()

    def index_regulatory_documents(self):
        """
        Build the regulatory knowledge base.
        """
        return self.indexer.index_regulatory_documents()

    def retrieve_context(self, query: str, top_k: int = 5):
        """
        Retrieve and format relevant regulatory evidence.
        """
        retrieval_results = self.retriever.retrieve(
            query=query,
            top_k=top_k
        )

        formatted_results = self.citation_engine.format_results(
            retrieval_results
        )

        return formatted_results

    def build_context_from_results(self, formatted_results):
        """
        Build a context string from retrieved citation records.
        """
        return self.citation_engine.build_context(
            formatted_results
        )

    def build_context(self, query: str, top_k: int = 5):
        """
        Build a context string suitable for an LLM prompt.
        """
        formatted_results = self.retrieve_context(
            query=query,
            top_k=top_k
        )

        return self.build_context_from_results(
            formatted_results
        )

    def extract_sources(self, formatted_results):
        """
        Extract unique source names from retrieved results.
        """
        sources = []

        for result in formatted_results:
            source_name = result.get("source", "Unknown")

            if source_name not in sources:
                sources.append(source_name)

        return sources

    def answer_with_context(self, query: str, top_k: int = 5):
        """
        Generate an AI-powered regulatory answer using retrieved context.
        """
        load_dotenv()

        formatted_results = self.retrieve_context(
            query=query,
            top_k=top_k
        )

        context = self.build_context_from_results(
            formatted_results
        )

        sources = self.extract_sources(
            formatted_results
        )

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""
You are CQVIP, an AI regulatory and validation assistant.

Answer the user's question using only the regulatory context provided below.
If the context does not contain enough information, say that the available knowledge base does not provide enough evidence.

User Question:
{query}

Regulatory Context:
{context}

Provide:
1. A clear answer
2. Key regulatory rationale
3. Sources referenced
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior CQV and GMP validation expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        answer = response.choices[0].message.content

        return {
            "question": query,
            "answer": answer,
            "sources": sources,
            "context": context,
            "retrieved_results": formatted_results
        }