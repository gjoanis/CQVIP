from app.exporters.oq_protocol import OQProtocolExporter

from app.models.project import Project
from app.models.asset import Asset
from app.models.document import Document

from app.parsers.urs_parser import URSParser

from app.services.qualification_engine import QualificationEngine
from app.services.traceability import TraceabilityService
from app.services.inspection import InspectionService
from app.services.test_generator import TestGenerator
from app.services.project_scanner import ProjectScanner
from app.services.project_loader import ProjectLoader

from app.reports.dashboard import DashboardReport
from app.reports.qualification_summary import QualificationSummaryReport
from app.exporters.excel_trace_matrix import ExcelTraceMatrix


def main():
    project = Project("BSD Expansion")

    washer = Asset(
        "Decontamination Washer",
        "Equipment"
    )

    scanner = ProjectScanner("documents")
    files = scanner.scan()

    project_loader = ProjectLoader()
    loaded_documents = project_loader.load_project(files)

    print("\nDISCOVERED DOCUMENTS")
    print("-" * 45)

    requirements = []
    urs = None

    for loaded_doc in loaded_documents:
        print("Filename:", loaded_doc["filename"])
        print("Type    :", loaded_doc["type"])
        print("-" * 45)

        if loaded_doc["type"] == "URS":
            urs = Document(
                loaded_doc["filename"],
                "URS"
            )

            parser = URSParser(loaded_doc["text"])
            requirements = parser.extract_requirements()

            for requirement in requirements:
                urs.add_requirement(requirement)

            washer.add_document(urs)

    if requirements:
        requirements[0].mark_verified("OQ-001")
        requirements[0].add_trace_link("FAT-001")
        requirements[0].add_trace_link("SAT-001")
        requirements[0].add_trace_link("IQ-001")

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

    excel = ExcelTraceMatrix(requirements)
    excel.export()

    oq = OQProtocolExporter(
        project,
        washer,
        requirements
    )

    oq.generate()

    dashboard.display()
    qualification_engine.display_dashboard()
    traceability.generate_matrix()
    traceability.gap_analysis()
    test_generator.display_tests()
    summary.generate()
    inspection.check_readiness()


if __name__ == "__main__":
    main()