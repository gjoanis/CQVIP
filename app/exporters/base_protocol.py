from app.exporters.word_document import WordDocumentExporter
from app.services.document_control import DocumentControl
from app.config.project_config import ProjectConfig


class BaseProtocolExporter:
    """
    Base class for all protocol exporters.
    """

    def __init__(self, project, asset, protocol_name, document_name):

        self.project = project
        self.asset = asset
        self.protocol_name = protocol_name
        self.document_name = document_name

    def create_document(self):

        config = ProjectConfig()
        control = DocumentControl(config)

        info = control.build(
            self.protocol_name.split()[0]
        )

        document = WordDocumentExporter(
            self.protocol_name,
            self.project.name,
            self.asset.name,
            info["document_number"]
        )

        document.add_title_page()

        document.add_section_heading("Document Information")

        document.add_paragraph(
            f"Project: {info['project']}"
        )

        document.add_paragraph(
            f"Document Number: {info['document_number']}"
        )

        document.add_paragraph(
            f"Revision: {info['revision']}"
        )

        document.add_paragraph(
            f"Status: {info['status']}"
        )

        document.add_paragraph(
            f"Prepared By: {info['prepared_by']}"
        )

        document.add_paragraph(
            f"Approved By: {info['approved_by']}"
        )

        document.add_paragraph(
            f"Date: {info['date']}"
        )

        document.add_approval_table()

        return document

    def save(self, document):

        document.save(self.document_name)