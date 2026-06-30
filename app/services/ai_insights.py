class AIInsights:
    """
    Rule-based AI insights supporting both Requirement objects
    and dictionaries.
    """

    def __init__(self, requirements):
        self.requirements = requirements

    def value(self, req, field, default=""):
        if isinstance(req, dict):
            return req.get(field, default)
        return getattr(req, field, default)

    def generate_project_summary(self):
        total = len(self.requirements)
        critical = self.count_critical_requirements()
        open_count = self.count_open_requirements()
        readiness = self.calculate_readiness_score()

        if total == 0:
            return "No URS uploaded."

        return (
            f"{total} requirements detected. "
            f"{critical} Critical/High requirements. "
            f"{open_count} remain open. "
            f"Inspection readiness is {readiness}%."
        )

    def generate_gap_analysis(self):
        gaps = []

        for req in self.requirements:
            if not self.value(req, "verified", False):
                phase = self.infer_phase(req)
                req_id = self.value(req, "req_id", "Unknown Requirement")

                gaps.append(
                    f"{req_id} requires verification during {phase}."
                )

        if not gaps:
            return "No gaps detected."

        return "\n".join(gaps)

    def generate_recommendations(self):
        recommendations = []

        for req in self.requirements:
            if self.value(req, "verified", False):
                continue

            req_id = self.value(req, "req_id", "Unknown Requirement")
            phase = self.infer_phase(req)
            criticality = self.value(req, "criticality", "")

            recommendations.append(
                f"{req_id}: Execute during {phase} and attach objective evidence."
            )

            if criticality in ["Critical", "High"]:
                recommendations.append(
                    f"{req_id}: PRIORITY - Critical/High GMP requirement."
                )

        if not recommendations:
            return "No recommendations."

        return "\n".join(recommendations[:10])

    def infer_phase(self, req):
        recommended = self.value(req, "recommended_verification", "")

        if not recommended:
            recommended = self.value(req, "recommended", "")

        if recommended:
            return recommended

        text = self.value(req, "text", "").lower()
        category = self.value(req, "category", "").lower()

        if "install" in text or "utility" in text:
            return "IQ"

        if (
            "alarm" in text
            or "interlock" in text
            or "record" in text
            or "data" in text
            or "safety" in text
        ):
            return "OQ"

        if (
            "clean" in text
            or "cycle" in text
            or "performance" in text
            or "pressure" in text
        ):
            return "PQ"

        if "training" in text:
            return "Training"

        if category in ["alarm", "safety", "data integrity"]:
            return "OQ"

        if category in ["cleaning", "environmental"]:
            return "PQ"

        return "OQ"

    def count_critical_requirements(self):
        return sum(
            1
            for req in self.requirements
            if self.value(req, "criticality", "") in ["Critical", "High"]
        )

    def count_open_requirements(self):
        return sum(
            1
            for req in self.requirements
            if not self.value(req, "verified", False)
        )

    def calculate_readiness_score(self):
        total = len(self.requirements)

        if total == 0:
            return 0

        open_count = self.count_open_requirements()

        return round(((total - open_count) / total) * 100)