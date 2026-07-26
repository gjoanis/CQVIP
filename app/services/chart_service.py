from collections import Counter


class ChartService:
    """
    Builds chart-ready data for the CQVIP executive dashboard.
    """

    def __init__(self, requirements):
        self.requirements = requirements

    def value(self, requirement, field, default=""):

        if isinstance(requirement, dict):
            return requirement.get(field, default)

        return getattr(requirement, field, default)

    def build_all_charts(self):

        return {

            "lifecycle_labels": self.get_lifecycle_labels(),

            "lifecycle_values": self.get_lifecycle_values(),

            "criticality_labels": self.get_criticality_labels(),

            "criticality_values": self.get_criticality_values(),

            "category_labels": self.get_category_labels(),

            "category_values": self.get_category_values(),

            "verification_labels": self.get_verification_labels(),

            "verification_values": self.get_verification_values(),

        }

    def get_lifecycle_counts(self):

        counter = Counter()

        for requirement in self.requirements:

            stage = self.value(
                requirement,
                "lifecycle_stage",
                "Unknown",
            )

            counter[stage] += 1

        return counter

    def get_category_counts(self):

        counter = Counter()

        for requirement in self.requirements:

            category = self.value(
                requirement,
                "category",
                "Uncategorized",
            )

            counter[category] += 1

        return counter

    def get_criticality_counts(self):

        counter = Counter()

        for requirement in self.requirements:

            criticality = self.value(
                requirement,
                "criticality",
                "Not Assigned",
            )

            counter[criticality] += 1

        return counter

    def get_verification_counts(self):

        counter = Counter()

        for requirement in self.requirements:

            verification = self.value(
                requirement,
                "recommended_verification",
                "Not Assigned",
            )

            counter[verification] += 1

        return counter

    def get_lifecycle_labels(self):
        return list(self.get_lifecycle_counts().keys())

    def get_lifecycle_values(self):
        return list(self.get_lifecycle_counts().values())

    def get_category_labels(self):
        return list(self.get_category_counts().keys())

    def get_category_values(self):
        return list(self.get_category_counts().values())

    def get_criticality_labels(self):
        return list(self.get_criticality_counts().keys())

    def get_criticality_values(self):
        return list(self.get_criticality_counts().values())

    def get_verification_labels(self):
        return list(self.get_verification_counts().keys())

    def get_verification_values(self):
        return list(self.get_verification_counts().values())