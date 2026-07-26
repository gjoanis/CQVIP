from pathlib import Path

from app.models.document import Document
from app.parsers.document_loader import DocumentLoader
from app.services.document_classifier import DocumentClassifier


class ProjectLoader:

    def __init__(self):

        self.loader = DocumentLoader()

    def load_project(self, files):

        project_documents = []

        for file in files:

            suffix = Path(file).suffix.lower()

            if suffix == ".docx":

                text = self.loader.load_docx(file)

            elif suffix == ".pdf":

                text = self.loader.load_pdf(file)

            elif suffix == ".txt":

                text = self.loader.load_txt(file)

            else:

                continue

            metadata = DocumentClassifier.classify(
                Path(file).name,
                text,
            )

            document = Document(

                system_id=None,

                lifecycle_stage_id=None,

                document_type_id=None,

                title=Path(file).name,

                filename=Path(file).name,

                original_filename=Path(file).name,

                file_path=str(file),

                uploaded_by="System",

            )

            document.text = text
            document.lifecycle_stage = metadata["lifecycle_stage"]
            document.document_type = metadata["document_type"]

            project_documents.append(document)

        return project_documents