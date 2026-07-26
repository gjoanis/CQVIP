class ReadinessEngine:

    def __init__(self, requirements):

        self.requirements = requirements

    def calculate(self):

        total = len(self.requirements)

        if total == 0:

            return {

                "overall_readiness": 0,

                "inspection_readiness": 0,

                "current_phase": "Planning & Requirements",

                "project_health": "Green",

                "phases": {},

            }

        lifecycle_stages = [

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

        phase_scores = {}

        for stage in lifecycle_stages:

            stage_requirements = [

                r

                for r in self.requirements

                if getattr(r, "lifecycle_stage", None) == stage

            ]

            if not stage_requirements:

                phase_scores[stage] = 0

                continue

            verified = sum(

                1

                for r in stage_requirements

                if getattr(r, "verified", False)

            )

            phase_scores[stage] = round(

                verified / len(stage_requirements) * 100

            )

        populated = [

            score

            for score in phase_scores.values()

            if score > 0

        ]

        overall = (

            round(sum(populated) / len(populated))

            if populated

            else 0

        )

        current_phase = "Completed"

        for stage in lifecycle_stages:

            if phase_scores[stage] < 100:

                current_phase = stage

                break

        if overall >= 85:

            health = "Green"

        elif overall >= 60:

            health = "Yellow"

        else:

            health = "Red"

        inspection = round(

            (

                phase_scores["Installation Qualification"]

                + phase_scores["Operational Qualification"]

                + phase_scores["Performance Qualification"]

            ) / 3

        )

        return {

            "overall_readiness": overall,

            "inspection_readiness": inspection,

            "current_phase": current_phase,

            "project_health": health,

            "phases": phase_scores,

        }