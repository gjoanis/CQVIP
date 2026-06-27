class AIInsights:
    """
    Rule-based AI-style insights for CQVIP Version 1.0.
    Generates project summary, gap analysis, and recommendations.
    """

    def __init__(self, requirements):
        self.requirements = requirements

    def generate_project_summary(self):
        total = len(self.requirements)
        critical = self.count_critical_requirements()
        open_count = self.count_open_requirements()
        readiness = self.calculate_readiness_score()

        if total == 0:
            return {
                "health": "No URS Uploaded",
                "summary": "Upload a URS document to begin requirement extraction.",
                "risk_level": "Not Assessed"
            }

        if readiness >= 80:
            health = "Good"
            risk = "Low"
        elif readiness >= 50:
            health = "Needs Review"
            risk = "Moderate"
        else:
            health = "At Risk"
            risk = "High"

        return {
            "health": health,
            "summary": (
                f"{total} requirements were detected. "
                f"{critical} requirements are classified as Critical. "
                f"{open_count} requirements remain open. "
                f"The current inspection readiness score is {readiness}%."
            ),
            "risk_level": risk
        }

    def generate_gap_analysis(self):
        gaps = []

        for req in self.requirements:
            req_id = req.get("req_id", "Unknown Requirement")
            phase = self.infer_phase(req)

            if req.get("verified", False) is False:
                gaps.append(
                    f"{req_id} remains open and requires verification during {phase}."
                )

        if not gaps:
            gaps.append("No open requirement gaps detected.")

        return gaps

    def generate_recommendations(self):
        recommendations = []

        for req in self.requirements:
            req_id = req.get("req_id", "Unknown Requirement")
            text = req.get("text", "").lower()
            category = req.get("category", "")
            criticality = req.get("criticality", "")
            phase = self.infer_phase(req)

            recommendations.append(
                f"{req_id}: Verify this requirement during {phase} and confirm objective evidence is captured."
            )

            if "alarm" in text or category == "Alarm":
                recommendations.append(
                    f"{req_id}: Confirm alarm activation, acknowledgement, and recording are tested."
                )

            if "data" in text or category == "Data Integrity":
                recommendations.append(
                    f"{req_id}: Review data integrity controls, record retention, and audit trail expectations."
                )

            if "safety" in text or "interlock" in text or category == "Safety":
                recommendations.append(
                    f"{req_id}: Confirm safety interlocks and fail-safe behavior are challenged."
                )

            if "clean" in text or "cycle" in text:
                recommendations.append(
                    f"{req_id}: Confirm cleaning cycle parameters and acceptance criteria are documented."
                )

            if criticality == "Critical":
                recommendations.append(
                    f"{req_id}: Prioritize this requirement because it may impact product quality, safety, or compliance."
                )

        if not recommendations:
            recommendations.append("No AI recommendations generated yet.")

        return recommendations[:10]

    def infer_phase(self, req):
        recommended = req.get("recommended", "")

        if recommended:
            return recommended

        text = req.get("text", "").lower()
        category = req.get("category", "").lower()

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

    def count_critical_requirements(self):
        return sum(
            1 for req in self.requirements
            if req.get("criticality", "") == "Critical"
        )

    def count_open_requirements(self):
        return sum(
            1 for req in self.requirements
            if req.get("verified", False) is False
        )

    def calculate_readiness_score(self):
        total = len(self.requirements)

        if total == 0:
            return 0

        open_count = self.count_open_requirements()

        return round(((total - open_count) / total) * 100)