from app.exporters.base_protocol import BaseProtocolExporter


class FATProtocolExporter(BaseProtocolExporter):

    def __init__(self, project, asset):

        super().__init__(
            project,
            asset,
            "Factory Acceptance Test Protocol",
            "FAT_Protocol.docx"
        )

    def generate(self):

        document = self.create_document()

        document.add_section_heading("Purpose")
        document.add_paragraph(
            "The purpose of the Factory Acceptance Test (FAT) is to verify "
            "that the equipment has been manufactured and operates according "
            "to the approved design specification prior to shipment."
        )

        document.add_responsibilities_table()
        document.add_prerequisites()
        document.add_equipment_required()
        document.add_safety_precautions()

        document.add_section_heading("Factory Acceptance Tests")

        checks = [
            "Verify equipment identification.",
            "Verify mechanical assembly.",
            "Verify electrical installation.",
            "Verify control system functionality.",
            "Verify alarm functionality.",
            "Verify safety interlocks.",
            "Verify operational sequences.",
            "Verify documentation package."
        ]

        document.add_test_execution_table(checks)

        document.add_approval_table()

        self.save(document)