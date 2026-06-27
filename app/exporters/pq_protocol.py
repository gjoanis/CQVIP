from app.exporters.base_protocol import BaseProtocolExporter
from app.intelligence.requirement_engine import RequirementEngine


class PQProtocolExporter(BaseProtocolExporter):

    def __init__(self, project, asset, requirements):

        super().__init__(
            project,
            asset,
            "Performance Qualification Protocol",
            "PQ_Protocol.docx"
        )

        self.requirements = requirements

    def generate(self):

        document = self.create_document()

        engine = RequirementEngine()

        document.add_section_heading("Purpose")
        document.add_paragraph(
            "The purpose of this Performance Qualification (PQ) protocol "
            "is to demonstrate that the equipment consistently performs "
            "as intended during routine operating conditions."
        )

        document.add_responsibilities_table()
        document.add_prerequisites()
        document.add_equipment_required()
        document.add_safety_precautions()

        document.add_section_heading("Performance Verification")

        for requirement in self.requirements:

            strategy = engine.analyze(requirement)

            document.add_section_heading(requirement.req_id)

            document.add_paragraph(
                f"Requirement:\n{requirement.text}"
            )

            checks = []

            for step in strategy["procedure"]:
                checks.append(step)

            document.add_test_execution_table(checks)

            document.add_paragraph("Acceptance Criteria:")

            for criterion in strategy["acceptance"]:
                document.add_paragraph(f"• {criterion}")

        document.add_approval_table()

        self.save(document)