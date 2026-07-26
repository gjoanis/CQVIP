from app.services.chart_service import ChartService
from app.services.ai_insights import AIInsights
from app.services.readiness_engine import ReadinessEngine


class DashboardService:

    def __init__(self, requirements):
        self.requirements = requirements

    def build(self):

        total = len(self.requirements)

        critical = sum(
            1
            for r in self.requirements
            if getattr(r, "criticality", "") in ["Critical", "High"]
        )

        open_requirements = sum(
            1
            for r in self.requirements
            if not getattr(r, "verified", False)
        )

        readiness = ReadinessEngine(
            self.requirements
        ).calculate()

        charts = ChartService(
            self.requirements
        )

        ai = AIInsights(
            self.requirements
        )

        lifecycle_summary = []

        stages = [
            "Planning & Requirements",
            "Design Qualification",
            "Factory Acceptance Testing",
            "Site Acceptance Testing",
            "Engineering Studies",
            "Commissioning",
            "Operational Readiness",
            "Installation Qualification",
            "Operational Qualification",
            "Performance Qualification",
            "Continued Verification",
            "Retirement",
        ]

        for stage in stages:

            docs = [
                r for r in self.requirements
                if getattr(r, "lifecycle_stage", None) == stage
            ]

            verified = sum(
                1
                for r in docs
                if getattr(r, "verified", False)
            )

            if len(docs) == 0:

                status = "Pending"

            elif verified == len(docs):

                status = "Complete"

            elif verified > 0:

                status = "In Progress"

            else:

                status = "Open"

            lifecycle_summary.append({

                "stage": stage,

                "status": status,

                "requirements": len(docs),

                "verified": verified,

            })

        return {

            "total_requirements": total,

            "critical_requirements": critical,

            "open_requirements": open_requirements,

            "quality_compliance_readiness": readiness["overall_readiness"],

            "inspection_readiness": readiness["inspection_readiness"],

            "current_phase": readiness["current_phase"],

            "project_health": readiness["project_health"],

            "phase_readiness": readiness["phases"],

            "requirements": self.requirements,

            "charts": charts.build_all_charts(),

            "ai_summary": ai.generate_project_summary(),

            "ai_gap_analysis": ai.generate_gap_analysis(),

            "ai_recommendations": ai.generate_recommendations(),

            "lifecycle": lifecycle_summary,

        }