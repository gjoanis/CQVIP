import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from app.knowledge import KnowledgeEngine


def main():
    knowledge = KnowledgeEngine()

    print("Indexing regulatory documents...")
    index_result = knowledge.index_regulatory_documents()
    print(index_result)

    print("\nAsking regulatory question...")
    query = "What does Annex 15 say about IQ OQ PQ qualification?"

    result = knowledge.answer_with_context(query=query, top_k=3)

    print("\nAI Answer:")
    print("=" * 80)
    print(result["answer"])
    print("=" * 80)

    print("\nStructured Sources:")
    print("=" * 80)
    for source in result["sources"]:
        print(f"- {source}")
    print("=" * 80)


if __name__ == "__main__":
    main()