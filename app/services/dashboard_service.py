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

        readiness = ReadinessEngine(self.requirements).calculate()

        charts = ChartService(self.requirements)

        ai = AIInsights(self.requirements)

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

            "lifecycle": [

                {
                    "stage": "Requirements Loaded",
                    "status": "Complete" if total > 0 else "Pending",
                },

                {
                    "stage": "Requirements Assigned",
                    "status":
                        "Complete" if total > 0 and all(
                            r.status in [
                                "Assigned",
                                "In Progress",
                                "Under Review",
                                "Verified",
                                "Approved",
                                "Closed"
                            ]
                            for r in self.requirements
                        )
                        else "In Progress" if any(
                            r.status in [
                                "Assigned",
                                "In Progress",
                                "Under Review",
                                "Verified",
                                "Approved",
                                "Closed"
                            ]
                            for r in self.requirements
                        )
                        else "Pending",
                },

                {
                    "stage": "Validation In Progress",
                    "status":
                        "Complete" if total > 0 and all(
                            r.status in [
                                "In Progress",
                                "Under Review",
                                "Verified",
                                "Approved",
                                "Closed"
                            ]
                            for r in self.requirements
                        )
                        else "In Progress" if any(
                            r.status in [
                                "In Progress",
                                "Under Review",
                                "Verified",
                                "Approved",
                                "Closed"
                            ]
                            for r in self.requirements
                        )
                        else "Pending",
                },

                {
                    "stage": "Technical Review",
                    "status":
                        "Complete" if total > 0 and all(
                            r.status in [
                                "Under Review",
                                "Verified",
                                "Approved",
                                "Closed"
                            ]
                            for r in self.requirements
                        )
                        else "In Progress" if any(
                            r.status in [
                                "Under Review",
                                "Verified",
                                "Approved",
                                "Closed"
                            ]
                            for r in self.requirements
                        )
                        else "Pending",
                },

                {
                    "stage": "Verification",
                    "status":
                        "Complete" if total > 0 and all(
                            r.status in [
                                "Verified",
                                "Approved",
                                "Closed"
                            ]
                            for r in self.requirements
                        )
                        else "In Progress" if any(
                            r.status in [
                                "Verified",
                                "Approved",
                                "Closed"
                            ]
                            for r in self.requirements
                        )
                        else "Pending",
                },

                {
                    "stage": "Approval",
                    "status":
                        "Complete" if total > 0 and all(
                            r.status in [
                                "Approved",
                                "Closed"
                            ]
                            for r in self.requirements
                        )
                        else "In Progress" if any(
                            r.status in [
                                "Approved",
                                "Closed"
                            ]
                            for r in self.requirements
                        )
                        else "Pending",
                },

                {
                    "stage": "Project Closed",
                    "status":
                        "Complete" if total > 0 and all(
                            r.status == "Closed"
                            for r in self.requirements
                        )
                        else "In Progress" if any(
                            r.status == "Closed"
                            for r in self.requirements
                        )
                        else "Pending",
                },

            ]

        }