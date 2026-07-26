from pathlib import Path


class DocumentClassifier:
    """
    Determines both the document type and lifecycle stage
    from the filename and document content.
    """

    DOCUMENT_MAP = {

        "URS": (
            "User Requirements Specification",
            "Planning & Requirements",
        ),

        "FRS": (
            "Functional Specification",
            "Design Qualification",
        ),

        "FS": (
            "Functional Specification",
            "Design Qualification",
        ),

        "DS": (
            "Design Specification",
            "Design Qualification",
        ),

        "DQ": (
            "Design Qualification",
            "Design Qualification",
        ),

        "RISK": (
            "Risk Assessment",
            "Planning & Requirements",
        ),

        "RA": (
            "Risk Assessment",
            "Planning & Requirements",
        ),

        "FAT": (
            "Factory Acceptance Test",
            "Factory Acceptance Testing",
        ),

        "SAT": (
            "Site Acceptance Test",
            "Site Acceptance Testing",
        ),

        "COMMISSIONING": (
            "Commissioning",
            "Commissioning",
        ),

        "IQ": (
            "Installation Qualification",
            "Installation Qualification",
        ),

        "OQ": (
            "Operational Qualification",
            "Operational Qualification",
        ),

        "PQ": (
            "Performance Qualification",
            "Performance Qualification",
        ),

        "CSV": (
            "Computer System Validation",
            "Operational Qualification",
        ),

        "SOP": (
            "Standard Operating Procedure",
            "Operational Readiness",
        ),

        "WI": (
            "Work Instruction",
            "Operational Readiness",
        ),

        "PM": (
            "Preventive Maintenance",
            "Continued Verification",
        ),

        "CAL": (
            "Calibration",
            "Continued Verification",
        ),

        "CC": (
            "Change Control",
            "Continued Verification",
        ),

        "DEVIATION": (
            "Deviation",
            "Continued Verification",
        ),

        "CAPA": (
            "CAPA",
            "Continued Verification",
        ),

        "TM": (
            "Training Record",
            "Operational Readiness",
        ),

        "QSR": (
            "Quality Record",
            "Operational Readiness",
        ),

        "DECOMMISSION": (
            "Decommissioning",
            "Retirement",
        ),

    }

    @classmethod
    def classify(cls, filename, text):

        filename = Path(filename).name.upper()

        for keyword, values in cls.DOCUMENT_MAP.items():

            if keyword in filename:

                return {

                    "document_type": values[0],

                    "lifecycle_stage": values[1],

                }

        text = text.upper()

        for keyword, values in cls.DOCUMENT_MAP.items():

            if keyword in text:

                return {

                    "document_type": values[0],

                    "lifecycle_stage": values[1],

                }

        return {

            "document_type": "Unknown",

            "lifecycle_stage": "Planning & Requirements",

        }