class InspectionService:
    """
    Determines whether an asset is inspection ready.
    """

    def __init__(self, asset):
        self.asset = asset

    def check_readiness(self):
        ready = True
        open_requirements = 0
        open_critical = 0

        for document in self.asset.documents:
            for requirement in document.requirements:
                if requirement.verified is False:
                    ready = False
                    open_requirements += 1

                    if requirement.criticality == "Critical":
                        open_critical += 1

        print("\nINSPECTION READINESS")
        print("-" * 45)

        print("Asset:", self.asset.name)
        print("Open Requirements:", open_requirements)
        print("Open Critical Requirements:", open_critical)

        if ready:
            print("Status: Inspection Ready")
        else:
            print("Status: Inspection NOT Ready")