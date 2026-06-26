from app.models.requirement import Requirement


class URSParser:
    """
    Extracts requirements from URS text.
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
        lines = self.text.split("\n")
        counter = 1

        for line in lines:
            line = line.strip()

            if line.lower().startswith("the"):
                category = self.categorize(line)
                verification = self.recommend_verification(category)
                criticality = self.assign_criticality(category)

                requirement = Requirement(
                    f"URS-{counter:03}",
                    line,
                    category
                )

                requirement.set_recommended_verification(verification)
                requirement.set_criticality(criticality)

                requirements.append(requirement)
                counter += 1

        return requirements