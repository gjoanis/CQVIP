from app.exporters.base_protocol import BaseProtocolExporter


class SATProtocolExporter(BaseProtocolExporter):

    def __init__(self, project, asset):

        super().__init__(
            project,
            asset,
            "Site Acceptance Test Protocol",
            "SAT_Protocol.docx"
        )

    def generate(self):

        document = self.create_document()

        document.add_section_heading("Purpose")
        document.add_paragraph(
            "The purpose of the Site Acceptance Test (SAT) is to verify "
            "that the equipment has been received, installed, and operates "
            "as intended at the user site."
        )

        document.add_responsibilities_table()
        document.add_prerequisites()
        document.add_equipment_required()
        document.add_safety_precautions()

        document.add_section_heading("Site Acceptance Tests")

        checks = [
            "Verify equipment receipt and condition.",
            "Verify equipment location.",
            "Verify installation at the user site.",
            "Verify utility connections.",
            "Verify communication with control systems.",
            "Verify alarms and interlocks.",
            "Verify startup operation.",
            "Verify site documentation package."
        ]

        document.add_test_execution_table(checks)

        document.add_approval_table()

        self.save(document)