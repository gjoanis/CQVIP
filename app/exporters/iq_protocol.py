from app.exporters.base_protocol import BaseProtocolExporter


class IQProtocolExporter(BaseProtocolExporter):

    def __init__(self, project, asset):

        super().__init__(
            project,
            asset,
            "Installation Qualification Protocol",
            "IQ_Protocol.docx"
        )

    def generate(self):

        document = self.create_document()

        document.add_section_heading("Purpose")
        document.add_paragraph(
            "The purpose of this Installation Qualification (IQ) protocol "
            "is to verify that the equipment has been installed according "
            "to approved drawings, specifications, and manufacturer recommendations."
        )

        document.add_section_heading("Scope")
        document.add_paragraph(
            f"This protocol applies to the installation qualification of "
            f"{self.asset.name}."
        )

        document.add_responsibilities_table()
        document.add_prerequisites()
        document.add_equipment_required()
        document.add_safety_precautions()

        document.add_section_heading("Installation Verification")

        checks = [
            "Verify equipment identification and asset tag.",
            "Verify equipment location and installation area.",
            "Verify utilities are connected as required.",
            "Verify major components are installed.",
            "Verify vendor documentation is available.",
            "Verify calibration status of applicable instruments.",
            "Verify applicable drawings are available.",
            "Verify software or control system version, if applicable."
        ]

        document.add_test_execution_table(checks)

        document.add_approval_table()

        self.save(document)