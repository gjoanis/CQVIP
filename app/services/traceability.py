class TraceabilityService:
    """
    Handles traceability and gap analysis.
    """

    def __init__(self, asset):
        self.asset = asset

    def generate_matrix(self):
        print("\nTRACEABILITY MATRIX")
        print("-" * 45)

        for document in self.asset.documents:
            for requirement in document.requirements:
                print("Requirement :", requirement.req_id)
                print("Text        :", requirement.text)
                print("Category    :", requirement.category)
                print("Criticality :", requirement.criticality)
                print("Recommended:", requirement.recommended_verification)
                print("Verified    :", requirement.verified)
                print("Verified By :", requirement.verified_by)

                for test in requirement.links.tests:
                    print("Trace Link  :", test)

                print("-" * 45)

    def gap_analysis(self):
        print("\nGAP ANALYSIS")
        print("-" * 45)

        gaps = 0

        for document in self.asset.documents:
            for requirement in document.requirements:
                if requirement.verified is False:
                    gaps += 1
                    print(requirement.req_id, "requires verification.")

        print("Open Gaps:", gaps)