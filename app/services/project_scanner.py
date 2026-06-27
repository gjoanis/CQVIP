from pathlib import Path


class ProjectScanner:
    """
    Scans a project folder and returns
    all supported validation documents.
    """

    SUPPORTED_TYPES = [
        ".docx",
        ".txt",
        ".pdf",
        ".xlsx"
    ]

    def __init__(self, folder):
        self.folder = Path(folder)

    def scan(self):

        documents = []

        if not self.folder.exists():
            return documents

        for file in self.folder.iterdir():

            if file.suffix.lower() in self.SUPPORTED_TYPES:
                documents.append(file)

        return sorted(documents)