from app.models.project import Project
from app.models.asset import Asset
from app.models.document import Document

from app.parsers.document_loader import DocumentLoader
from app.parsers.urs_parser import URSParser

from app.services.qualification_engine import QualificationEngine
from app.services.traceability import TraceabilityService
from app.services.inspection import InspectionService
from app.services.test_generator import TestGenerator

from app.reports.dashboard import DashboardReport
from app.reports.qualification_summary import QualificationSummaryReport

from app.services.project_scanner import ProjectScanner
from app.services.project_loader import ProjectLoader

def main():
    scanner = ProjectScanner("documents")
    files = scanner.scan()

    loader = ProjectLoader()
    loaded_documents = loader.load_project(files)

    print("\nDISCOVERED DOCUMENTS")
    print("-" * 45)

    for doc in loaded_documents:
        print("Filename:", doc["filename"])
        print("Type    :", doc["type"])
        print("-" * 45)

    project = Project("BSD Expansion")

    washer = Asset(
        "Decontamination Washer",
        "Equipment"
    )

    urs = Document(
        "URS - Decontamination Washer",
        "URS"
    )

    loader = DocumentLoader()
    urs_text = loader.load_docx("documents/sample_urs.docx")

    parser = URSParser(urs_text)
    requirements = parser.extract_requirements()

    for requirement in requirements:
        urs.add_requirement(requirement)

    requirements[0].mark_verified("OQ-001")
    requirements[0].add_trace_link("FAT-001")
    requirements[0].add_trace_link("SAT-001")
    requirements[0].add_trace_link("IQ-001")

    washer.add_document(urs)
    project.add_asset(washer)

    qualification_engine = QualificationEngine()
    qualification_engine.complete("URS")
    qualification_engine.complete("SIA")
    qualification_engine.complete("FAT")
    qualification_engine.complete("SAT")
    qualification_engine.complete("Commissioning")
    qualification_engine.complete("IQ")
    qualification_engine.complete("OQ")
    qualification_engine.complete("PQ")
    qualification_engine.complete("QSR")
    qualification_engine.complete("Released")

    dashboard = DashboardReport(project, washer)
    traceability = TraceabilityService(washer)
    inspection = InspectionService(washer)
    test_generator = TestGenerator(requirements)
    summary = QualificationSummaryReport(
        project,
        washer,
        qualification_engine
    )

    test_generator.generate_tests()

    dashboard.display()
    qualification_engine.display_dashboard()
    traceability.generate_matrix()
    traceability.gap_analysis()
    test_generator.display_tests()
    summary.generate()
    inspection.check_readiness()


if __name__ == "__main__":
    main()