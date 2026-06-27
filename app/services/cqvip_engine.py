from app.config.project_config import ProjectConfig

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
from app.services.validation_package import ValidationPackage

from app.reports.dashboard import DashboardReport

from app.exporters.excel_trace_matrix import ExcelTraceMatrix
from app.exporters.iq_protocol import IQProtocolExporter
from app.exporters.oq_protocol import OQProtocolExporter
from app.exporters.pq_protocol import PQProtocolExporter
from app.exporters.fat_protocol import FATProtocolExporter
from app.exporters.sat_protocol import SATProtocolExporter
from app.exporters.commissioning_protocol import CommissioningProtocolExporter
from app.exporters.qualification_summary_report import QualificationSummaryReportExporter


class CQVIPEngine:
    """
    Main orchestration engine for CQVIP.
    """

    def __init__(self, documents_folder="documents"):
        self.config = ProjectConfig()
        self.documents_folder = documents_folder

        self.project = Project(
            self.config.PROJECT_NAME
        )

        self.asset = Asset(
            self.config.ASSET_NAME,
            self.config.ASSET_TYPE
        )

        self.requirements = []

        self.qualification_engine = QualificationEngine()

    def load_documents(self):
        scanner = ProjectScanner(self.documents_folder)
        files = scanner.scan()

        loader = ProjectLoader()
        loaded_documents = loader.load_project(files)

        print("\nDISCOVERED DOCUMENTS")
        print("-" * 45)

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
                    self.requirements.append(requirement)

                self.asset.add_document(urs)

        if self.requirements:
            self.requirements[0].mark_verified("OQ-001")
            self.requirements[0].add_trace_link("IQ-001")
            self.requirements[0].add_trace_link("FAT-001")
            self.requirements[0].add_trace_link("SAT-001")

        self.project.add_asset(self.asset)

    def complete_lifecycle(self):
        stages = [
            "URS",
            "SIA",
            "FAT",
            "SAT",
            "Commissioning",
            "IQ",
            "OQ",
            "PQ",
            "QSR",
            "Released"
        ]

        for stage in stages:
            self.qualification_engine.complete(stage)

    def generate_documents(self):
        test_generator = TestGenerator(self.requirements)
        test_generator.generate_tests()

        excel = ExcelTraceMatrix(self.requirements)

        iq = IQProtocolExporter(
            self.project,
            self.asset
        )

        oq = OQProtocolExporter(
            self.project,
            self.asset,
            self.requirements
        )

        pq = PQProtocolExporter(
            self.project,
            self.asset,
            self.requirements
        )

        fat = FATProtocolExporter(
            self.project,
            self.asset
        )

        sat = SATProtocolExporter(
            self.project,
            self.asset
        )

        commissioning = CommissioningProtocolExporter(
            self.project,
            self.asset
        )

        summary = QualificationSummaryReportExporter(
            self.project,
            self.asset,
            self.qualification_engine,
            self.requirements
        )

        excel.export()
        iq.generate()
        oq.generate()
        pq.generate()
        fat.generate()
        sat.generate()
        commissioning.generate()
        summary.generate()

        validation_package = ValidationPackage()
        validation_package.add(excel)
        validation_package.add(iq)
        validation_package.add(oq)
        validation_package.add(pq)
        validation_package.add(fat)
        validation_package.add(sat)
        validation_package.add(commissioning)
        validation_package.add(summary)
        validation_package.build()

    def display_reports(self):
        dashboard = DashboardReport(
            self.project,
            self.asset
        )

        traceability = TraceabilityService(self.asset)
        inspection = InspectionService(self.asset)
        test_generator = TestGenerator(self.requirements)

        dashboard.display()
        self.qualification_engine.display_dashboard()
        traceability.generate_matrix()
        traceability.gap_analysis()

        test_generator.generate_tests()
        test_generator.display_tests()

        inspection.check_readiness()

    def run(self):
        self.load_documents()
        self.complete_lifecycle()
        self.generate_documents()
        self.display_reports()