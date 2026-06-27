class AIInsights:
    """
    Rule-based AI-style insights for CQVIP Version 1.0.

    This does not call an external AI API yet.
    It creates executive summaries, gap analysis, and recommendations
    from the parsed URS requirements.
    """

    def __init__(self, requirements):
        self.requirements = requirements

    def generate_project_summary(self):
        total_requirements = len(self.requirements)
        critical_requirements = self.count_critical_requirements()
        open_requirements = self.count_open_requirements()
        readiness_score = self.calculate_readiness_score()

        if total_requirements == 0:
            return {
                "health": "No URS uploaded",
                "summary": "Upload a URS document to begin requirement extraction and validation package generation.",
                "risk_level": "Not assessed"
            }

        if readiness_score >= 80:
            health = "Good"
            risk_level = "Low"
        elif readiness_score >= 50:
            health = "Needs Review"
            risk_level = "Moderate"
        else:
            health = "At Risk"
            risk_level = "High"

        summary = (
            f"{total_requirements} requirements were detected. "
            f"{critical_requirements} requirements are classified as Critical. "
            f"{open_requirements} requirements remain open. "
            f"The current inspection readiness score is {readiness_score}%."
        )

        return {
            "health": health,
            "summary": summary,
            "risk_level": risk_level
        }

    def generate_gap_analysis(self):
        gaps = []

        for requirement in self.requirements:
            req_id = requirement.get("req_id", "")
            recommended = requirement.get("recommended", "")
            verified = requirement.get("verified", False)

            if verified is False:
                gaps.append(
                    f"{req_id} remains open and requires verification during {recommended}."
                )

        if not gaps:
            gaps.append("No open requirement gaps detected.")

        return gaps

    def generate_recommendations(self):
        recommendations = []

        for requirement in self.requirements:
            req_id = requirement.get("req_id", "")
            category = requirement.get("category", "")
            criticality = requirement.get("criticality", "")
            recommended = requirement.get("recommended", "")

            if criticality == "Critical":
                recommendations.append(
                    f"{req_id}: Prioritize this requirement because it is classified as Critical."
                )

            if "OQ" in recommended:
                recommendations.append(
                    f"{req_id}: Confirm functional challenge testing is included in OQ."
                )

            if "PQ" in recommended:
                recommendations.append(
                    f"{req_id}: Confirm performance-based acceptance criteria are defined for PQ."
                )

            if "IQ" in recommended:
                recommendations.append(
                    f"{req_id}: Confirm installation verification evidence is documented in IQ."
                )

            if category == "Data Integrity":
                recommendations.append(
                    f"{req_id}: Review audit trail, record retention, user access, and data integrity controls."
                )

            if category == "Safety":
                recommendations.append(
                    f"{req_id}: Confirm safety interlocks, alarms, and fail-safe behavior are challenged."
                )

            if category == "Alarm":
                recommendations.append(
                    f"{req_id}: Confirm alarm activation, acknowledgement, and recording are verified."
                )

        if not recommendations:
            recommendations.append("No AI recommendations generated yet.")

        return recommendations[:10]

    def count_critical_requirements(self):
        count = 0

        for requirement in self.requirements:
            if requirement.get("criticality", "") == "Critical":
                count += 1

        return count

    def count_open_requirements(self):
        count = 0

        for requirement in self.requirements:
            if requirement.get("verified", False) is False:
                count += 1

        return count

    def calculate_readiness_score(self):
        total_requirements = len(self.requirements)

        if total_requirements == 0:
            return 0

        open_requirements = self.count_open_requirements()

        readiness_score = round(
            ((total_requirements - open_requirements) / total_requirements) * 100
        )

        return readiness_score
