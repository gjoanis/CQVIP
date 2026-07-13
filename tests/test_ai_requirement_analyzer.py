import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from app.services.ai_requirement_analyzer import AIRequirementAnalyzer


def main():
    analyzer = AIRequirementAnalyzer()

    requirement = "The system shall maintain secure electronic records with audit trails for all GMP-relevant data changes."

    print("Analyzing requirement with RAG...")
    result = analyzer.analyze(requirement)

    print("\nAnalysis Result:")
    print("=" * 80)
    print(result)
    print("=" * 80)


if __name__ == "__main__":
    main()