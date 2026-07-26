class QualificationEngine:
    """
    Controls lifecycle qualification progression using the CQVIP lifecycle.
    """

    def __init__(self):

        self.stages = {

            "Planning & Requirements": False,

            "Design Qualification": False,

            "Factory Acceptance Testing": False,

            "Site Acceptance Testing": False,

            "Engineering Studies": False,

            "Commissioning": False,

            "Operational Readiness": False,

            "Installation Qualification": False,

            "Operational Qualification": False,

            "Performance Qualification": False,

            "Continued Verification": False,

            "Retirement": False,

        }

        self.rules = {

            "Design Qualification": [
                "Planning & Requirements"
            ],

            "Factory Acceptance Testing": [
                "Design Qualification"
            ],

            "Site Acceptance Testing": [
                "Factory Acceptance Testing"
            ],

            "Engineering Studies": [
                "Site Acceptance Testing"
            ],

            "Commissioning": [
                "Engineering Studies"
            ],

            "Operational Readiness": [
                "Commissioning"
            ],

            "Installation Qualification": [
                "Operational Readiness"
            ],

            "Operational Qualification": [
                "Installation Qualification"
            ],

            "Performance Qualification": [
                "Operational Qualification"
            ],

            "Continued Verification": [
                "Performance Qualification"
            ],

            "Retirement": [
                "Continued Verification"
            ],

        }

    def can_complete(self, stage):

        if stage not in self.rules:
            return True

        for prerequisite in self.rules[stage]:

            if not self.stages.get(prerequisite, False):

                print(f"Cannot complete {stage}")
                print(f"Missing prerequisite: {prerequisite}")

                return False

        return True

    def complete(self, stage):

        if stage not in self.stages:
            return

        if self.can_complete(stage):
            self.stages[stage] = True

    def complete_all(self):

        for stage in self.stages:

            self.complete(stage)

    def is_complete(self, stage):

        return self.stages.get(stage, False)

    def dashboard(self):

        return [

            {
                "stage": stage,
                "complete": status,
            }

            for stage, status in self.stages.items()

        ]

    def display_dashboard(self):

        print("\nQUALIFICATION DASHBOARD")
        print("-" * 50)

        for stage, status in self.stages.items():

            symbol = "✓" if status else "○"

            print(f"{symbol} {stage}")