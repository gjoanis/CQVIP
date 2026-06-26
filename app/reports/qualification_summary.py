class QualificationSummaryReport:
    """
    Generates a qualification summary report for an asset.
    """

    def __init__(self, project, asset, qualification_engine):
        self.project = project
        self.asset = asset
        self.qualification_engine = qualification_engine

    def generate(self):
        print("\nQUALIFICATION SUMMARY REPORT")
        print("=" * 45)

        print("Project:", self.project.name)
        print("Asset:", self.asset.name)
        print("Asset Type:", self.asset.asset_type)

        total_requirements = 0
        verified_requirements = 0
        open_requirements = 0

        for document in self.asset.documents:
            for requirement in document.requirements:
                total_requirements += 1

                if requirement.verified:
                    verified_requirements += 1
                else:
                    open_requirements += 1

        print("\nRequirement Summary")
        print("-" * 45)
        print("Total Requirements:", total_requirements)
        print("Verified Requirements:", verified_requirements)
        print("Open Requirements:", open_requirements)

        print("\nLifecycle Summary")
        print("-" * 45)

        for stage, status in self.qualification_engine.stages.items():
            result = "Complete" if status else "Open"
            print(stage + ":", result)

        print("\nFinal Disposition")
        print("-" * 45)

        if open_requirements == 0 and self.qualification_engine.stages["Released"]:
            print("System is qualified and released for intended use.")
        else:
            print("System is not ready for final release.")