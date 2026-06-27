from app.exporters.qualification_summary_report import QualificationSummaryReportExporter
from app.models.project import Project
from app.models.asset import Asset
from app.models.document import Document
from app.config.project_config import ProjectConfig
from app.parsers.urs_parser import URSParser

from app.services.qualification_engine import QualificationEngine
from app.services.traceability import TraceabilityService
from app.services.inspection import InspectionService
from app.services.test_generator import TestGenerator
from app.services.project_scanner import ProjectScanner
from app.services.project_loader import ProjectLoader
from app.services.validation_package import ValidationPackage

from app.reports.dashboard import DashboardReport
from app.reports.qualification_summary import QualificationSummaryReport

from app.exporters.excel_trace_matrix import ExcelTraceMatrix
from app.exporters.iq_protocol import IQProtocolExporter
from app.exporters.oq_protocol import OQProtocolExporter
from app.exporters.pq_protocol import PQProtocolExporter
from app.exporters.fat_protocol import FATProtocolExporter
from app.exporters.sat_protocol import SATProtocolExporter
from app.exporters.commissioning_protocol import CommissioningProtocolExporter


def main():

    # -------------------------------------------------
    # Project
    # -------------------------------------------------

    config = ProjectConfig()
    project = Project (
        config.PROJECT_NAME
    )

    asset = Asset(
        config.ASSET_NAME,
        config.ASSET_TYPE
    )

    # -------------------------------------------------
    # Load Documents
    # -------------------------------------------------

    scanner = ProjectScanner("documents")
    files = scanner.scan()

    loader = ProjectLoader()
    loaded_documents = loader.load_project(files)

    print("\nDISCOVERED DOCUMENTS")
    print("-" * 45)

    requirements = []

    for loaded_doc in loaded_documents:

        print("Filename:", loaded_doc["filename"])
        print("Type    :", loaded_doc["type"])
        print("-" * 45)

        if loaded_doc["type"] == "URS":

            urs = Document(
                loaded_doc["filename"],
                "URS"
            )

            parser = URSParser(
                loaded_doc["text"]
            )

            parsed_requirements = parser.extract_requirements()

            for requirement in parsed_requirements:
                urs.add_requirement(requirement)
                requirements.append(requirement)

            asset.add_document(urs)

    # -------------------------------------------------
    # Demo Verification
    # -------------------------------------------------

    if requirements:

        requirements[0].mark_verified("OQ-001")

        requirements[0].add_trace_link("IQ-001")
        requirements[0].add_trace_link("FAT-001")
        requirements[0].add_trace_link("SAT-001")

    project.add_asset(asset)

    # -------------------------------------------------
    # Qualification Status
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Services
    # -------------------------------------------------

    dashboard = DashboardReport(
        project,
        asset
    )

    traceability = TraceabilityService(asset)

    inspection = InspectionService(asset)

    test_generator = TestGenerator(
        requirements
    )

    summary = QualificationSummaryReportExporter(
        project,
        asset,
        qualification_engine,
        requirements
    )

    test_generator.generate_tests()

    # -------------------------------------------------
    # Exporters
    # -------------------------------------------------

    excel = ExcelTraceMatrix(requirements)

    iq = IQProtocolExporter(
        project,
        asset
    )

    oq = OQProtocolExporter(
        project,
        asset,
        requirements
    )

    pq = PQProtocolExporter(
        project,
        asset,
        requirements
    )

    fat = FATProtocolExporter(
        project,
        asset,
        requirements
    )

    sat = SATProtocolExporter(
        project,
        asset,
        requirements
    )

    commissioning = CommissioningProtocolExporter(
        project,
        asset,
        requirements
    )

    # -------------------------------------------------
    # Generate Validation Documents
    # -------------------------------------------------

    excel.export()

    iq.generate()

    oq.generate()

    pq.generate()

    fat.generate()

    sat.generate()

    commissioning.generate()

    summary.generate()

    # -------------------------------------------------
    # Validation Package
    # -------------------------------------------------

    validation_package = ValidationPackage()

    validation_package.add(excel)
    validation_package.add(iq)
    validation_package.add(oq)
    validation_package.add(pq)
    validation_package.add(fat)
    validation_package.add(sat)
    validation_package.add(commissioning)

    validation_package.build()

    # -------------------------------------------------
    # Reports
    # -------------------------------------------------

    dashboard.display()

    qualification_engine.display_dashboard()

    traceability.generate_matrix()

    traceability.gap_analysis()

    test_generator.display_tests()

    inspection.check_readiness()


if __name__ == "__main__":
    main()