class ReadinessEngine:

    def __init__(self, requirements):

        self.requirements = requirements

    def calculate(self):

        total = len(self.requirements)

        if total == 0:

            return {
                "overall_readiness": 0,
                "inspection_readiness": 0,
                "current_phase": "Phase 1",
                "project_health": "Green",
                "phases": {
                    "phase1": 0,
                    "phase2": 0,
                    "phase3": 0,
                    "phase4": 0,
                    "phase5": 0,
                },
            }

        phase1 = self.phase1()
        phase2 = self.phase2()
        phase3 = self.phase3()
        phase4 = self.phase4()
        phase5 = self.phase5()

        overall = round(
            (
                phase1
                + phase2
                + phase3
                + phase4
                + phase5
            ) / 5
        )

        if phase5 < 100:
            current_phase = "Phase 5"

        elif phase4 < 100:
            current_phase = "Phase 4"

        elif phase3 < 100:
            current_phase = "Phase 3"

        elif phase2 < 100:
            current_phase = "Phase 2"

        else:
            current_phase = "Phase 1"

        if overall >= 85:
            health = "Green"

        elif overall >= 60:
            health = "Yellow"

        else:
            health = "Red"

        return {

            "overall_readiness": overall,

            "inspection_readiness": phase4,

            "current_phase": current_phase,

            "project_health": health,

            "phases": {

                "phase1": phase1,

                "phase2": phase2,

                "phase3": phase3,

                "phase4": phase4,

                "phase5": phase5,

            },

        }

    def phase1(self):

        completed = 0

        for req in self.requirements:

            if (
                req.category
                and req.criticality
                and req.recommended_verification
            ):
                completed += 1

        return round(completed / len(self.requirements) * 100)

    def phase2(self):

        completed = 0

        for req in self.requirements:

            if req.risk and req.gmp_reference:

                completed += 1

        return round(completed / len(self.requirements) * 100)

    def phase3(self):

        completed = 0

        for req in self.requirements:

            if req.status in [

                "Assigned",

                "Under Review",

                "Verified",

                "Closed",

            ]:

                completed += 1

        return round(completed / len(self.requirements) * 100)

    def phase4(self):

        completed = 0

        for req in self.requirements:

            if req.verified:

                completed += 1

        return round(completed / len(self.requirements) * 100)

    def phase5(self):

        completed = 0

        for req in self.requirements:

            if req.status == "Closed":

                completed += 1

        return round(completed / len(self.requirements) * 100)