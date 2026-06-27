from app.exporters.base_protocol import BaseProtocolExporter


class CommissioningProtocolExporter(BaseProtocolExporter):

    def __init__(self, project, asset):

        super().__init__(
            project,
            asset,
            "Commissioning Protocol",
            "Commissioning_Protocol.docx"
        )

    def generate(self):

        document = self.create_document()

        document.add_section_heading("Purpose")
        document.add_paragraph(
            "The purpose of this Commissioning Protocol is to verify "
            "that the equipment has been installed, connected, and started "
            "up in a controlled manner prior to formal qualification."
        )

        document.add_responsibilities_table()
        document.add_prerequisites()
        document.add_equipment_required()
        document.add_safety_precautions()

        document.add_section_heading("Commissioning Verification")

        checks = [
            "Verify equipment installation is complete.",
            "Verify utilities are available and connected.",
            "Verify equipment startup can be performed safely.",
            "Verify basic functional operation.",
            "Verify alarms and safety devices.",
            "Verify required documentation is available.",
            "Verify system is ready for qualification."
        ]

        document.add_test_execution_table(checks)

        document.add_approval_table()

        self.save(document)