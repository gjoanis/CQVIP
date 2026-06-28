import re

from app.models.requirement import Requirement


class URSParser:
    """
    Extracts requirements from URS text.
    Supports auto-numbered requirements and existing IDs like URS-001 or REQ-001.
    """

    def __init__(self, text):
        self.text = text

    def categorize(self, requirement_text):
        text = requirement_text.lower()

        if "alarm" in text:
            return "Alarm"
        elif "temperature" in text or "pressure" in text:
            return "Environmental"
        elif "clean" in text:
            return "Cleaning"
        elif "data" in text or "record" in text:
            return "Data Integrity"
        elif "operator" in text or "training" in text:
            return "Operational"
        elif "safety" in text:
            return "Safety"
        else:
            return "Functional"

    def recommend_verification(self, category):
        if category == "Alarm":
            return "OQ"
        elif category == "Cleaning":
            return "OQ / PQ"
        elif category == "Data Integrity":
            return "CSV / OQ"
        elif category == "Environmental":
            return "OQ"
        elif category == "Safety":
            return "OQ"
        elif category == "Operational":
            return "SOP / Training"
        else:
            return "Commissioning / IQ / OQ"

    def assign_criticality(self, category):
        if category in ["Alarm", "Safety", "Data Integrity"]:
            return "Critical"
        elif category in ["Cleaning", "Environmental"]:
            return "Major"
        else:
            return "Minor"

    def extract_requirements(self):
        requirements = []
        counter = 1

        text = self.text.replace("\r", "")

        pattern = re.compile(
            r"(URS-\d+|REQ-\d+|FRS-\d+|DS-\d+)?\s*(.*?shall.*?)(?=\n\s*\n|\n[A-Z][A-Za-z ]+:|\Z)",
            re.IGNORECASE | re.DOTALL
        )

        for match in pattern.finditer(text):

            req_id = match.group(1)
            req_text = match.group(2).strip()

            req_text = re.sub(r"\s+", " ", req_text)

            if not req_id:
                req_id = f"URS-{counter:03}"

            category = self.categorize(req_text)
            verification = self.recommend_verification(category)
            criticality = self.assign_criticality(category)

            requirement = Requirement(
                req_id,
                req_text,
                category
            )

            requirement.set_recommended_verification(verification)
            requirement.set_criticality(criticality)

            requirements.append(requirement)

            counter += 1

        return requirements