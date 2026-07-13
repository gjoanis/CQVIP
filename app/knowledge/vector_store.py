"""
CQVIP Vector Store

Simple local JSON-based vector store for Python 3.14 compatibility.
"""

import json
import math
from pathlib import Path


class VectorStore:
    def __init__(self, persist_path: str = "knowledge_base/vector_db/regulatory_vectors.json"):
        self.persist_path = Path(persist_path)
        self.persist_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.persist_path.exists():
            self._save([])

    def _load(self):
        with open(self.persist_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, records):
        with open(self.persist_path, "w", encoding="utf-8") as f:
            json.dump(records, f)

    def add_chunks(self, embedded_chunks):
        records = self._load()

        for chunk in embedded_chunks:
            records.append(
                {
                    "id": chunk["chunk_id"],
                    "text": chunk["text"],
                    "embedding": chunk["embedding"],
                    "metadata": {
                        "source": chunk["source"],
                        "path": chunk["path"],
                    },
                }
            )

        self._save(records)

    def search(self, query_embedding, top_k: int = 5):
        records = self._load()

        scored = []

        for record in records:
            score = self._cosine_similarity(
                query_embedding,
                record["embedding"]
            )

            scored.append((score, record))

        scored.sort(key=lambda x: x[0], reverse=True)

        top_results = scored[:top_k]

        return {
            "documents": [[item[1]["text"] for item in top_results]],
            "metadatas": [[item[1]["metadata"] for item in top_results]],
            "distances": [[1 - item[0] for item in top_results]],
        }

    def count(self):
        return len(self._load())

    def reset(self):
        self._save([])

    def _cosine_similarity(self, a, b):
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))

        if norm_a == 0 or norm_b == 0:
            return 0

        return dot / (norm_a * norm_b)