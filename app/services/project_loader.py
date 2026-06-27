from app.parsers.document_loader import DocumentLoader
from app.services.document_classifier import DocumentClassifier


class ProjectLoader:

    def __init__(self):
        self.loader = DocumentLoader()

    def load_project(self, files):

        project_documents = []

        for file in files:

            suffix = file.suffix.lower()

            if suffix == ".docx":
                text = self.loader.load_docx(file)

            elif suffix == ".txt":
                text = self.loader.load_txt(file)

            else:
                continue

            document_type = DocumentClassifier.classify(
                file.name,
                text
            )

            project_documents.append({
                "filename": file.name,
                "type": document_type,
                "text": text
            })

        return project_documents