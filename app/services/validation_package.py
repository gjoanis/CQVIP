import os
import shutil


class ValidationPackage:
    """
    Collects generated CQVIP deliverables into one package folder
    and creates a ZIP archive.
    """

    def __init__(self):
        self.documents = []

        self.base_dir = os.getcwd()

        self.output_folder = os.path.join(
            self.base_dir,
            "exports",
            "Validation_Package"
        )

        self.zip_name = os.path.join(
            self.base_dir,
            "exports",
            "Validation_Package"
        )

    def add(self, document):
        self.documents.append(document)

    def build(self):
        print("\nBUILDING VALIDATION PACKAGE")
        print("-" * 50)

        os.makedirs(self.output_folder, exist_ok=True)

        generated_files = [
            "Traceability_Matrix.xlsx",
            "IQ_Protocol.docx",
            "OQ_Protocol.docx",
            "PQ_Protocol.docx",
            "FAT_Protocol.docx",
            "SAT_Protocol.docx",
            "Commissioning_Protocol.docx",
            "Qualification_Summary_Report.docx"
        ]

        for filename in generated_files:

            source = os.path.join(
                self.base_dir,
                filename
            )

            if os.path.exists(source):

                destination = os.path.join(
                    self.output_folder,
                    filename
                )

                shutil.copy2(
                    source,
                    destination
                )

                print(f"Added: {filename}")

            else:
                print(f"Missing: {source}")

        shutil.make_archive(
            self.zip_name,
            "zip",
            self.output_folder
        )

        print("\nValidation Package Complete")
        print(f"Package Folder: {self.output_folder}")
        print(f"ZIP Created: {self.zip_name}.zip")