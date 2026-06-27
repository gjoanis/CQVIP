from app.exporters.word_document import WordDocumentExporter


class IQProtocolExporter:

    def __init__(self, project, asset):
        self.project = project
        self.asset = asset

    def generate(self):
        document = WordDocumentExporter(
            "Installation Qualification Protocol",
            self.project.name,
            self.asset.name,
            "IQ"
        )

        document.add_title_page()
        document.add_document_information()
        document.add_approval_table()

        document.add_section_heading("Purpose")
        document.add_paragraph(
            "The purpose of this Installation Qualification (IQ) protocol is to verify "
            "that the equipment has been installed according to approved specifications, "
            "drawings, vendor documentation, and applicable GMP requirements."
        )

        document.add_section_heading("Scope")
        document.add_paragraph(
            "This protocol applies to the installation verification of the "
            f"{self.asset.name} for the {self.project.name} project."
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
        document.save("IQ_Protocol.docx")