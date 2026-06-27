class AIInsights:
    """
    Rule-based AI-style insights for CQVIP Version 1.0.
    Generates project summary, gap analysis, and qualification recommendations.
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
            if req.get("verified", False):
                continue

            req_id = req.get("req_id", "Unknown Requirement")
            text = req.get("text", "").lower()
            category = req.get("category", "")
            criticality = req.get("criticality", "")
            phase = self.infer_phase(req)

            if category == "Cleaning" or "clean" in text or "cycle" in text:
                recommendations.append(
                    f"{req_id}: Execute a full cleaning cycle during {phase}, document cycle parameters, and attach objective evidence."
                )

            elif category == "Alarm" or "alarm" in text:
                recommendations.append(
                    f"{req_id}: Challenge the alarm logic, verify alarm acknowledgement, and document alarm response."
                )

            elif category == "Data Integrity" or "data" in text or "record" in text:
                recommendations.append(
                    f"{req_id}: Verify audit trail functionality, record retention, user access, and 21 CFR Part 11 expectations."
                )

            elif category == "Safety" or "safety" in text or "interlock" in text:
                recommendations.append(
                    f"{req_id}: Execute safety interlock testing and document fail-safe operation."
                )

            elif category == "Environmental" or "pressure" in text:
                recommendations.append(
                    f"{req_id}: Verify operating conditions remain within validated environmental or process limits."
                )

            elif category == "Operational" or "training" in text or "operator" in text:
                recommendations.append(
                    f"{req_id}: Confirm operator training is completed and training records are approved before release."
                )

            else:
                recommendations.append(
                    f"{req_id}: Execute this requirement during {phase}, document objective evidence, and link results to the traceability matrix."
                )

            if criticality == "Critical":
                recommendations.append(
                    f"{req_id}: Prioritize this requirement because it may impact product quality, patient safety, or GMP compliance."
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

        if "training" in text or "operator" in text:
            return "Training"

        if category in ["alarm", "safety", "data integrity"]:
            return "OQ"

        if category in ["cleaning", "environmental"]:
            return "PQ"

        if category == "operational":
            return "Training"

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