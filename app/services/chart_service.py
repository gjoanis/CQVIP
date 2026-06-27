from collections import Counter


class ChartService:
    """
    Builds chart-ready data for the CQVIP executive dashboard.

    The output is designed to be used directly by Chart.js in index.html.
    """

    def __init__(self, requirements):
        self.requirements = requirements

    def build_all_charts(self):
        return {
            "phase_labels": self.get_phase_labels(),
            "phase_values": self.get_phase_values(),
            "criticality_labels": self.get_criticality_labels(),
            "criticality_values": self.get_criticality_values(),
            "category_labels": self.get_category_labels(),
            "category_values": self.get_category_values()
        }

    def infer_phase(self, requirement):
        recommended = requirement.get("recommended", "")

        if recommended:
            return recommended

        text = requirement.get("text", "").lower()
        category = requirement.get("category", "").lower()

        if "install" in text or "utility" in text:
            return "IQ"

        if "alarm" in text or "interlock" in text or "record" in text or "data" in text:
            return "OQ"

        if "clean" in text or "cycle" in text or "performance" in text:
            return "PQ"

        if "training" in text:
            return "Training"

        if category in ["alarm", "safety", "data integrity"]:
            return "OQ"

        return "OQ"

    def get_phase_counts(self):
        phase_counter = Counter()

        for requirement in self.requirements:
            phase = self.infer_phase(requirement)

            if phase:
                phase_counter[phase] += 1

        return phase_counter

    def get_criticality_counts(self):
        criticality_counter = Counter()

        for requirement in self.requirements:
            criticality = requirement.get("criticality", "")

            if criticality:
                criticality_counter[criticality] += 1

        return criticality_counter

    def get_category_counts(self):
        category_counter = Counter()

        for requirement in self.requirements:
            category = requirement.get("category", "")

            if category:
                category_counter[category] += 1

        return category_counter

    def get_phase_labels(self):
        return list(self.get_phase_counts().keys())

    def get_phase_values(self):
        return list(self.get_phase_counts().values())

    def get_criticality_labels(self):
        return list(self.get_criticality_counts().keys())

    def get_criticality_values(self):
        return list(self.get_criticality_counts().values())

    def get_category_labels(self):
        return list(self.get_category_counts().keys())

    def get_category_values(self):
        return list(self.get_category_counts().values())
