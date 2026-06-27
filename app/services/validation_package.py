import os
import shutil


class ValidationPackage:

    def __init__(self):

        self.documents = []

        self.output_folder = os.path.join(
            "exports",
            "Validation_Package"
        )

    def add(self, document):
        self.documents.append(document)

    def build(self):

        print("\nBUILDING VALIDATION PACKAGE")
        print("-" * 50)

        os.makedirs(
            self.output_folder,
            exist_ok=True
        )

        generated_files = [

            "IQ_Protocol.docx",

            "OQ_Protocol.docx",

            "PQ_Protocol.docx",

            "FAT_Protocol.docx",

            "SAT_Protocol.docx",

            "Commissioning_Protocol.docx",

            "Qualification_Summary_Report.docx",

            "Traceability_Matrix.xlsx"

        ]

        for filename in generated_files:

            if os.path.exists(filename):

                destination = os.path.join(
                    self.output_folder,
                    filename
                )

                shutil.copy(
                    filename,
                    destination
                )

                print(f"Added: {filename}")

        print("\nValidation Package Complete")

        print(self.output_folder)