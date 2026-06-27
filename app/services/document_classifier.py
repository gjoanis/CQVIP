from pathlib import Path


class DocumentClassifier:
    """
    Determines the document type based on
    filename and document content.
    """

    DOCUMENT_TYPES = [
        "URS",
        "FRS",
        "FS",
        "DS",
        "RA",
        "FAT",
        "SAT",
        "COMMISSIONING",
        "IQ",
        "OQ",
        "PQ",
        "CSV",
        "SOP",
        "TM",
        "QSR"
    ]

    @staticmethod
    def classify(filename, text):

        filename = filename.upper()

        for doc_type in DocumentClassifier.DOCUMENT_TYPES:
            if doc_type in filename:
                return doc_type

        text = text.upper()

        for doc_type in DocumentClassifier.DOCUMENT_TYPES:
            if doc_type in text:
                return doc_type

        return "UNKNOWN"