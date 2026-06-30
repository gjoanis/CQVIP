from collections import Counter


class ChartService:
    """
    Builds chart-ready data for the CQVIP executive dashboard.
    Works with both Requirement objects and dictionaries.
    """

    def __init__(self, requirements):
        self.requirements = requirements

    def value(self, requirement, field, default=""):
        """
        Safely read either an object attribute or dictionary key.
        """
        if isinstance(requirement, dict):
            return requirement.get(field, default)

        return getattr(requirement, field, default)

    def build_all_charts(self):
        return {
            "phase_labels": self.get_phase_labels(),
            "phase_values": self.get_phase_values(),
            "criticality_labels": self.get_criticality_labels(),
            "criticality_values": self.get_criticality_values(),
            "category_labels": self.get_category_labels(),
            "category_values": self.get_category_values(),
        }

    def infer_phase(self, requirement):
        recommended = self.value(requirement, "recommended", "")

        if recommended:
            return recommended

        text = self.value(requirement, "text", "").lower()
        category = self.value(requirement, "category", "").lower()

        if "install" in text or "utility" in text:
            return "IQ"

        if (
            "alarm" in text
            or "interlock" in text
            or "record" in text
            or "data" in text
        ):
            return "OQ"

        if (
            "clean" in text
            or "cycle" in text
            or "performance" in text
        ):
            return "PQ"

        if "training" in text:
            return "Training"

        if category in ["alarm", "safety", "data integrity"]:
            return "OQ"

        return "OQ"

    def get_phase_counts(self):
        counter = Counter()

        for requirement in self.requirements:
            counter[self.infer_phase(requirement)] += 1

        return counter

    def get_criticality_counts(self):
        counter = Counter()

        for requirement in self.requirements:
            criticality = self.value(requirement, "criticality", "")

            if criticality:
                counter[criticality] += 1

        return counter

    def get_category_counts(self):
        counter = Counter()

        for requirement in self.requirements:
            category = self.value(requirement, "category", "")

            if category:
                counter[category] += 1

        return counter

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