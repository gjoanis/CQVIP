from app.services.readiness_engine import ReadinessEngine


class AIInsights:

    def __init__(self, requirements):

        self.requirements = requirements

    def value(self, req, field, default=""):

        if isinstance(req, dict):
            return req.get(field, default)

        return getattr(req, field, default)

    def generate_project_summary(self):

        readiness = ReadinessEngine(
            self.requirements
        ).calculate()

        total = len(self.requirements)

        if total == 0:

            return (
                "No project data is available. "
                "Upload lifecycle documents to begin building the digital validation package."
            )

        overall = readiness["overall_readiness"]
        inspection = readiness["inspection_readiness"]
        phase = readiness["current_phase"]
        health = readiness["project_health"]

        critical = self.count_critical_requirements()
        open_items = self.count_open_requirements()

        summary = (

            f"Overall Lifecycle Readiness is {overall}%. "

            f"The current lifecycle stage is {phase}. "

            f"Inspection Readiness is {inspection}%. "

            f"Project Health is {health}. "

        )

        if critical:

            summary += (
                f"{critical} Critical or High-risk requirements remain. "
            )

        if open_items:

            summary += (
                f"{open_items} requirements are still awaiting verification. "
            )

        if overall >= 90:

            summary += (
                "The validation package is approaching inspection readiness."
            )

        elif overall >= 70:

            summary += (
                "The project is progressing well with several remaining verification activities."
            )

        elif overall >= 50:

            summary += (
                "Execution is underway, but compliance gaps still require attention."
            )

        else:

            summary += (
                "The project is in the early stages of the validation lifecycle."
            )

        return summary

    def generate_gap_analysis(self):

        gaps = []

        for req in self.requirements:

            verified = self.value(
                req,
                "verified",
                False,
            )

            lifecycle = self.value(
                req,
                "lifecycle_stage",
                "Unknown",
            )

            document = self.value(
                req,
                "document_type",
                "Unknown",
            )

            req_id = self.value(
                req,
                "req_id",
                "",
            )

            category = self.value(
                req,
                "category",
                "",
            )

            criticality = self.value(
                req,
                "criticality",
                "",
            )

            status = self.value(
                req,
                "status",
                "Open",
            )

            if verified:

                gap = "None"
                risk = "Low"
                recommendation = "Requirement verified."
                priority = "Complete"

            else:

                gap = "Verification Evidence Missing"

                if criticality in ["Critical", "High"]:

                    risk = "High"
                    priority = "Critical"

                elif criticality == "Medium":

                    risk = "Medium"
                    priority = "Medium"

                else:

                    risk = "Low"
                    priority = "Low"

                recommendation = (
                    f"Complete verification within the {lifecycle} stage and update the {document}."
                )

            gaps.append({

                "requirement": req_id,

                "lifecycle": lifecycle,

                "document": document,

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

            return (
                "No recommendations. The current lifecycle documentation appears complete."
            )

        return "\n".join(recommendations[:10])

    def count_critical_requirements(self):

        return sum(

            1

            for req in self.requirements

            if self.value(
                req,
                "criticality",
                "",
            ) in ["Critical", "High"]

        )

    def count_open_requirements(self):

        return sum(

            1

            for req in self.requirements

            if not self.value(
                req,
                "verified",
                False,
            )

        )
