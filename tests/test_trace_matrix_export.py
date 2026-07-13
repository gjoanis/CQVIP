import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.models.requirement import Requirement
from app.services.test_generator import TestGenerator
from app.exporters.excel_trace_matrix import ExcelTraceMatrix


def main():
    requirement = Requirement(
        "URS-001",
        "The Washroom shall have a Purified Water point of use.",
        "Utility Qualification"
    )

    requirement.criticality = "High"
    requirement.recommended_verification = "Lifecycle Qualification"
    requirement.acceptance_criteria = "POU is installed and operational."

    requirements = [requirement]

    generator = TestGenerator(requirements)
    generator.generate_tests()

    exporter = ExcelTraceMatrix(requirements)
    exporter.export("Traceability_Matrix_DEV.xlsx")

    print(requirement.lifecycle_tests)
    print("Development trace matrix created successfully.")


if __name__ == "__main__":
    main()