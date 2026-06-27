from app.exporters.word_document import WordDocumentExporter


class QualificationSummaryReportExporter:

    def __init__(self, project, asset, qualification_engine, requirements):
        self.project = project
        self.asset = asset
        self.engine = qualification_engine
        self.requirements = requirements

    def generate(self):

        document = WordDocumentExporter(
            "Qualification Summary Report",
            self.project.name,
            self.asset.name,
            "QSR"
        )

        # --------------------------------------------------
        # Title Page
        # --------------------------------------------------

        document.add_title_page()
        document.add_document_information()
        document.add_approval_table()

        # --------------------------------------------------
        # Purpose
        # --------------------------------------------------

        document.add_section_heading("Purpose")

        document.add_paragraph(
            "The purpose of this Qualification Summary Report is to "
            "summarize the qualification activities performed and "
            "document the final qualification status of the system."
        )

        # --------------------------------------------------
        # Scope
        # --------------------------------------------------

        document.add_section_heading("Scope")

        document.add_paragraph(
            f"This report summarizes qualification activities "
            f"performed for {self.asset.name}."
        )

        # --------------------------------------------------
        # Requirement Summary
        # --------------------------------------------------

        total = len(self.requirements)
        verified = sum(1 for r in self.requirements if r.verified)
        open_items = total - verified

        document.add_section_heading("Requirement Summary")

        document.add_paragraph(f"Total Requirements: {total}")
        document.add_paragraph(f"Verified Requirements: {verified}")
        document.add_paragraph(f"Open Requirements: {open_items}")

        # --------------------------------------------------
        # Qualification Status
        # --------------------------------------------------

        document.add_section_heading("Qualification Status")

        document.add_section_heading("Qualification Status")

        for stage, completed in self.engine.stages.items():
            status = "Complete" if completed else "Open"

            document.add_paragraph(
                f"{stage}: {status}"
            )

        # --------------------------------------------------
        # Final Assessment
        # --------------------------------------------------

        document.add_section_heading("Final Assessment")

        if open_items == 0:
            document.add_paragraph(
                "All qualification requirements have been successfully "
                "verified. The system is recommended for release."
            )
        else:
            document.add_paragraph(
                "Open qualification items remain. The system is not "
                "recommended for release until outstanding items are "
                "resolved."
            )

        # --------------------------------------------------
        # Approval
        # --------------------------------------------------

        document.add_approval_table()

        document.save("Qualification_Summary_Report.docx")