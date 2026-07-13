"""
Regulatory Document Loader

Loads regulatory guidance documents from the CQVIP knowledge base.
Supports PDF and TXT files.
"""

from pathlib import Path
from pypdf import PdfReader


class RegulatoryLoader:
    """
    Loads regulatory documents from knowledge_base/regulatory_docs.
    """

    def __init__(self, regulatory_docs_path: str = "knowledge_base/regulatory_docs"):
        self.regulatory_docs_path = Path(regulatory_docs_path)

    def load_documents(self):
        documents = []

        if not self.regulatory_docs_path.exists():
            self.regulatory_docs_path.mkdir(parents=True, exist_ok=True)
            return documents

        for file_path in self.regulatory_docs_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() == ".txt":
                documents.append(self._load_txt(file_path))

            elif file_path.is_file() and file_path.suffix.lower() == ".pdf":
                documents.extend(self._load_pdf(file_path))

        return documents

    def _get_authority(self, file_path: Path):
        """
        Authority is based on folder name: FDA, EMA, ICH, etc.
        """
        try:
            return file_path.parent.name
        except Exception:
            return "Unknown"

    def _load_txt(self, file_path: Path):
        text = file_path.read_text(encoding="utf-8", errors="ignore")

        return {
            "authority": self._get_authority(file_path),
            "source": file_path.name,
            "path": str(file_path),
            "page": None,
            "text": text,
        }

    def _load_pdf(self, file_path: Path):
        documents = []
        reader = PdfReader(str(file_path))

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            if text.strip():
                documents.append(
                    {
                        "authority": self._get_authority(file_path),
                        "source": file_path.name,
                        "path": str(file_path),
                        "page": page_number,
                        "text": text,
                    }
                )

        return documents