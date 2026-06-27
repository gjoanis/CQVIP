from openpyxl import Workbook


class ExcelTraceMatrix:
    """
    Exports requirements into an Excel traceability matrix.
    """

    def __init__(self, requirements):
        self.requirements = requirements

    def export(self, filename="Traceability_Matrix.xlsx"):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Trace Matrix"

        worksheet.append([
            "Requirement ID",
            "Requirement",
            "Category",
            "Criticality",
            "Recommended Verification",
            "Verified",
            "Verified By",
            "Trace Links"
        ])

        for requirement in self.requirements:
            worksheet.append([
                requirement.req_id,
                requirement.text,
                requirement.category,
                requirement.criticality,
                requirement.recommended_verification,
                "Yes" if requirement.verified else "No",
                requirement.verified_by,
                ", ".join(requirement.links.tests)
            ])

        workbook.save(filename)

        print(f"\nExcel Trace Matrix saved as {filename}")