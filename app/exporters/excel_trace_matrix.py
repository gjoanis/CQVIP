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
            "DQ",
            "FAT",
            "SAT",
            "Commissioning",
            "IQ",
            "OQ",
            "PQ",
            "Verified",
            "Verified By"
        ])

        for requirement in self.requirements:
            worksheet.append([
                requirement.req_id,
                requirement.text,
                requirement.category,
                requirement.criticality,
                requirement.recommended_verification,
                ", ".join(requirement.lifecycle_tests["DQ"]),
                ", ".join(requirement.lifecycle_tests["FAT"]),
                ", ".join(requirement.lifecycle_tests["SAT"]),
                ", ".join(requirement.lifecycle_tests["Commissioning"]),
                ", ".join(requirement.lifecycle_tests["IQ"]),
                ", ".join(requirement.lifecycle_tests["OQ"]),
                ", ".join(requirement.lifecycle_tests["PQ"]),
                "Yes" if requirement.verified else "No",
                requirement.verified_by
            ])

        workbook.save(filename)

        print(f"\nExcel Trace Matrix saved as {filename}")