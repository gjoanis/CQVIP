"""
CQVIP Citation Engine

Formats retrieved regulatory document chunks into
clean, user-friendly citations.
"""


class CitationEngine:
    """
    Converts raw retrieval results into formatted citations.
    """

    def format_results(self, retrieval_results):
        """
        Format ChromaDB retrieval results.

        Args:
            retrieval_results (dict): Raw results returned from VectorStore.search()

        Returns:
            list[dict]: Formatted citation records.
        """

        formatted = []

        documents = retrieval_results.get("documents", [[]])[0]
        metadatas = retrieval_results.get("metadatas", [[]])[0]
        distances = retrieval_results.get("distances", [[]])

        if distances:
            distances = distances[0]
        else:
            distances = [None] * len(documents)

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            formatted.append(
                {
                    "source": metadata.get("source", "Unknown"),
                    "path": metadata.get("path", ""),
                    "content": document,
                    "similarity": distance,
                }
            )

        return formatted

    def build_context(self, formatted_results):
        """
        Build a single context string for the LLM prompt.
        """

        context = ""

        for result in formatted_results:

            context += (
                f"\nSource: {result['source']}\n"
                f"{result['content']}\n"
            )

        return context.strip()