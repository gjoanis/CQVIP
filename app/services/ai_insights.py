from app.services.readiness_engine import ReadinessEngine


class AIInsights:
    """
    AI-generated project insights supporting Requirement objects
    and dictionaries.
    """

    def __init__(self, requirements):
        self.requirements = requirements

    def value(self, req, field, default=""):
        if isinstance(req, dict):
            return req.get(field, default)
        return getattr(req, field, default)

    def generate_project_summary(self):

        readiness = ReadinessEngine(self.requirements).calculate()

        overall = readiness["overall_readiness"]
        inspection = readiness["inspection_readiness"]
        phase = readiness["current_phase"]
        health = readiness["project_health"]

        total = len(self.requirements)

        critical = self.count_critical_requirements()

        open_items = self.count_open_requirements()

        if total == 0:
            return (
                "No project data is currently available. "
                "Upload a URS to begin calculating Quality Compliance Readiness."
            )

        summary = (
            f"Overall Quality Compliance Readiness is {overall}%. "
            f"The project is currently in {phase}. "
            f"Inspection Readiness is {inspection}%. "
            f"Project Health is {health}. "
        )

        if critical > 0:
            summary += (
                f"There are {critical} Critical/High GMP requirements requiring close attention. "
            )

        if open_items > 0:
            summary += (
                f"{open_items} requirements still require verification before project completion. "
            )

        if overall >= 90:
            summary += (
                "The project is approaching inspection readiness with only minor activities remaining."
            )

        elif overall >= 70:
            summary += (
                "The project is progressing well but additional verification activities are required before release."
            )

        elif overall >= 50:
            summary += (
                "Execution is underway, however several compliance gaps remain that should be prioritized."
            )

        else:
            summary += (
                "The project is still in the early stages of the compliance lifecycle and significant work remains."
            )

        return summary

    def generate_gap_analysis(self):

        gaps = []

        for req in self.requirements:

            verified = self.value(req, "verified", False)

            req_id = self.value(req, "req_id", "")

            category = self.value(req, "category", "")

            criticality = self.value(req, "criticality", "")

            status = self.value(req, "status", "Open")

            phase = self.infer_phase(req)

            if verified:

                gap = "None"

                risk = "Low"

                recommendation = "Requirement is fully verified."

                priority = "Complete"

            else:

                gap = "Evidence Missing"

                if criticality in ["Critical", "High"]:

                    risk = "High"

                    recommendation = (
                        f"Complete {phase} verification and upload objective evidence."
                    )

                    priority = "Critical"

                elif criticality == "Medium":

                    risk = "Medium"

                    recommendation = (
                        f"Complete {phase} verification."
                    )

                    priority = "Medium"

                else:

                    risk = "Low"

                    recommendation = (
                        f"Complete {phase} verification."
                    )

                    priority = "Low"

            gaps.append({

                "requirement": req_id,

                "category": category,

                "criticality": criticality,

                "status": status,

                "gap": gap,

                "risk": risk,

                "recommendation": recommendation,

                "priority": priority,

            })

        return gaps

    def generate_recommendations(self):

        recommendations = []

        for gap in self.generate_gap_analysis():

            if gap["priority"] == "Complete":
                continue

            recommendations.append(

                f"{gap['requirement']}: {gap['recommendation']}"

            )

        if not recommendations:

            return "No recommendations. Project is ready for release."

        return "\n".join(recommendations[:10])

    def infer_phase(self, req):

        recommended = self.value(
            req,
            "recommended_verification",
            ""
        )

        if recommended:
            return recommended

        text = self.value(req, "text", "").lower()

        if "install" in text or "utility" in text:
            return "IQ"

        if (
            "alarm" in text
            or "interlock" in text
            or "record" in text
            or "software" in text
            or "data" in text
        ):
            return "OQ"

        if (
            "process" in text
            or "performance" in text
            or "clean" in text
            or "cycle" in text
        ):
            return "PQ"

        return "OQ"

    def count_critical_requirements(self):

        return sum(

            1

            for req in self.requirements

            if self.value(
                req,
                "criticality",
                ""
            ) in ["Critical", "High"]

        )

    def count_open_requirements(self):

        return sum(

            1

            for req in self.requirements

            if not self.value(
                req,
                "verified",
                False
            )

        )
