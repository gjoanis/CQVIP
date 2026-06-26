class QualificationEngine:
    """
    Controls lifecycle qualification stage rules.
    """

    def __init__(self):
        self.stages = {
            "URS": False,
            "SIA": False,
            "FS": False,
            "DS": False,
            "FAT": False,
            "SAT": False,
            "Commissioning": False,
            "IQ": False,
            "OQ": False,
            "PQ": False,
            "QSR": False,
            "Released": False
        }

        self.rules = {
            "SAT": ["FAT"],
            "IQ": ["Commissioning"],
            "OQ": ["IQ"],
            "PQ": ["IQ", "OQ"],
            "QSR": ["IQ", "OQ", "PQ"],
            "Released": ["QSR"]
        }

    def can_complete(self, stage):
        if stage not in self.rules:
            return True

        for required_stage in self.rules[stage]:
            if self.stages[required_stage] is False:
                print("Cannot complete", stage)
                print("Missing prerequisite:", required_stage)
                return False

        return True

    def complete(self, stage):
        if stage in self.stages:
            if self.can_complete(stage):
                self.stages[stage] = True

    def display_dashboard(self):
        print("\nQUALIFICATION DASHBOARD")
        print("-" * 45)

        for stage, status in self.stages.items():
            symbol = "✓" if status else "○"
            print(symbol, stage)