from app.exporters.word_document import WordDocumentExporter
from app.intelligence.requirement_engine import RequirementEngine


class PQProtocolExporter:

    def __init__(self, project, asset, requirements):
        self.project = project
        self.asset = asset
        self.requirements = requirements

    def generate(self):

        engine = RequirementEngine()

        document = WordDocumentExporter(
            "Performance Qualification Protocol",
            self.project.name,
            self.asset.name,
            "PQ"
        )

        document.add_title_page()
        document.add_document_information()
        document.add_approval_table()

        document.add_section_heading("Purpose")
        document.add_paragraph(
            "The purpose of this Performance Qualification (PQ) protocol "
            "is to demonstrate that the equipment consistently performs "
            "as intended under routine operating conditions."
        )

        document.add_section_heading("Scope")
        document.add_paragraph(
            f"This protocol applies to the performance qualification of "
            f"{self.asset.name}."
        )

        document.add_responsibilities_table()
        document.add_prerequisites()
        document.add_equipment_required()
        document.add_safety_precautions()

        document.add_section_heading("Performance Qualification Tests")

        for requirement in self.requirements:

            strategy = engine.analyze(requirement)

            document.add_section_heading(requirement.req_id)

            document.add_paragraph(
                f"Requirement:\n{requirement.text}"
            )

            document.add_paragraph(
                f"Objective:\n{strategy['objective']}"
            )

            document.add_paragraph("Procedure:")

            for step in strategy["procedure"]:
                document.add_paragraph(f"- {step}")

            document.add_test_execution_table(
                strategy["procedure"]
            )

            document.add_paragraph("Acceptance Criteria")

            for criterion in strategy["acceptance"]:
                document.add_paragraph(f"• {criterion}")

            document.add_paragraph("Required Evidence")

            for evidence in strategy["evidence"]:
                document.add_paragraph(f"• {evidence}")

        document.add_approval_table()

        document.save("PQ_Protocol.docx")