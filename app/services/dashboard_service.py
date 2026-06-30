from app.services.chart_service import ChartService
from app.services.ai_insights import AIInsights


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

        readiness = (
            round(
                ((total - open_requirements) / total) * 100
            )
            if total
            else 0
        )

        if readiness >= 80:
            status = "Inspection Ready"
        elif readiness >= 50:
            status = "Needs Review"
        else:
            status = "Not Ready"

        charts = ChartService(self.requirements)

        ai = AIInsights(self.requirements)

        return {

            "total_requirements": total,

            "critical_requirements": critical,

            "open_requirements": open_requirements,

            "readiness_score": readiness,

            "readiness_status": status,

            "requirements": self.requirements,

            "charts": charts.build_all_charts(),

            "ai_summary": ai.generate_project_summary(),

            "ai_gap_analysis": ai.generate_gap_analysis(),

            "ai_recommendations": ai.generate_recommendations(),

            "lifecycle": [

                {
                    "stage": "URS",
                    "status": "Complete",
                },

                {
                    "stage": "DQ",
                    "status": "Pending",
                },

                {
                    "stage": "FAT",
                    "status": "Pending",
                },

                {
                    "stage": "SAT",
                    "status": "Pending",
                },

                {
                    "stage": "Commissioning",
                    "status": "Pending",
                },

                {
                    "stage": "IQ",
                    "status": "Pending",
                },

                {
                    "stage": "OQ",
                    "status": "Pending",
                },

                {
                    "stage": "PQ",
                    "status": "Pending",
                }

            ]

        }