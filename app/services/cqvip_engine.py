from pathlib import Path

from app.config.project_config import ProjectConfig

from app.models.asset import Asset
from app.models.document import Document
from app.models.project import Project

from app.parsers.urs_parser import URSParser

from app.services.document_classifier import DocumentClassifier
from app.services.project_loader import ProjectLoader
from app.services.qualification_engine import QualificationEngine
from app.services.traceability import TraceabilityService
from app.services.inspection import InspectionService
from app.services.test_generator import TestGenerator


class CQVIPEngine:
    """
    Core orchestration engine for the CQVIP lifecycle platform.
    """

    def __init__(self, documents_folder="documents"):

        self.config = ProjectConfig()

        self.documents_folder = documents_folder

        self.reset_project()

    def reset_project(self):

        self.project = Project(self.config.PROJECT_NAME)

        self.asset = Asset(

            self.config.ASSET_NAME,

            self.config.ASSET_TYPE,

        )

        self.requirements = []

        self.qualification_engine = QualificationEngine()

    def load_documents(self):

        folder = Path(self.documents_folder)

        files = [

            file

            for file in folder.iterdir()

            if file.is_file()

        ]

        self._load_files(files)

    def load_single_document(self, filepath):

        self._load_files([Path(filepath)])

    def _load_files(self, files):

        loader = ProjectLoader()

        documents = loader.load_project(files)

        print("\nDISCOVERED DOCUMENTS")
        print("=" * 80)

        for loaded_document in documents:

            metadata = DocumentClassifier.classify(

                loaded_document.name,

                loaded_document.text,

            )

            document = Document(

                system_id=None,

                lifecycle_stage_id=None,

                document_type_id=None,

                filename=loaded_document.filename,

                file_path="",

                title=loaded_document.name,

            )

            document.document_type = metadata["document_type"]

            document.lifecycle_stage = metadata["lifecycle_stage"]

            print(f"{document.name}")

            print(f"Type   : {document.document_type}")

            print(f"Stage  : {document.lifecycle_stage}")

            if document.document_type == "User Requirements Specification":

                parser = URSParser(

                    loaded_document.text

                )

                parsed = parser.extract_requirements()

                for requirement in parsed:

                    requirement.document_name = document.name

                    requirement.document_type = document.document_type

                    requirement.lifecycle_stage = document.lifecycle_stage

                    document.add_requirement(requirement)

                    self.requirements.append(requirement)

            self.asset.add_document(document)

        self.project.add_asset(self.asset)

    def complete_lifecycle(self):

        for stage in [

            "Planning & Requirements",

            "Design Qualification",

            "Factory Acceptance Testing",

            "Site Acceptance Testing",

            "Commissioning",

            "Installation Qualification",

            "Operational Qualification",

            "Performance Qualification",

            "Continued Verification",

        ]:

            self.qualification_engine.complete(stage)

    def display_reports(self):

        TraceabilityService(

            self.asset

        ).generate_matrix()

        TraceabilityService(

            self.asset

        ).gap_analysis()

        TestGenerator(

            self.requirements

        ).generate_tests()

        InspectionService(

            self.asset

        ).check_readiness()

    def run(self):

        self.reset_project()

        self.load_documents()

        self.complete_lifecycle()

        self.display_reports()

    def run_for_file(self, filepath):

        self.reset_project()

        self.load_single_document(filepath)

        self.complete_lifecycle()

        self.display_reports()