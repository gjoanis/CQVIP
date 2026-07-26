class TraceabilityService:
    """
    Generates lifecycle traceability matrices and gap analysis.
    """

    def __init__(self, asset):
        self.asset = asset

    def generate_matrix(self):

        print("\nLIFECYCLE TRACEABILITY MATRIX")
        print("=" * 80)

        for document in self.asset.documents:

            print(f"\nDocument: {document.name}")

            if hasattr(document, "document_type"):
                print(f"Type: {document.document_type}")

            if hasattr(document, "lifecycle_stage"):
                print(f"Lifecycle Stage: {document.lifecycle_stage}")

            print("-" * 80)

            for requirement in document.requirements:

                print(f"Requirement        : {requirement.req_id}")

                if getattr(requirement, "source_req_id", None):
                    print(f"Source Requirement : {requirement.source_req_id}")

                print(f"Category           : {requirement.category}")

                print(f"Criticality        : {requirement.criticality}")

                print(f"Verification       : {requirement.recommended_verification}")

                print(f"Status             : {requirement.status}")

                print(f"Verified           : {requirement.verified}")

                print(f"Verified By        : {requirement.verified_by}")

                print(f"GMP Reference      : {requirement.gmp_reference}")

                print(f"Acceptance Criteria: {requirement.acceptance_criteria}")

                if requirement.regulatory_sources:

                    print("Regulatory Sources")

                    for source in requirement.regulatory_sources:
                        print(f"  • {source}")

                if requirement.regulatory_rationale:

                    print("Regulatory Rationale")

                    print(requirement.regulatory_rationale)

                if requirement.links.tests:

                    print("Verification Evidence")

                    for test in requirement.links.tests:
                        print(f"  • {test}")

                print("-" * 80)

    def gap_analysis(self):

        print("\nLIFECYCLE GAP ANALYSIS")
        print("=" * 80)

        gaps = 0

        for document in self.asset.documents:

            for requirement in document.requirements:

                if requirement.verified:
                    continue

                gaps += 1

                print(f"{requirement.req_id}")

                if getattr(requirement, "source_req_id", None):
                    print(f"Source Requirement : {requirement.source_req_id}")

                if hasattr(document, "document_type"):
                    print(f"Document Type      : {document.document_type}")

                if hasattr(document, "lifecycle_stage"):
                    print(f"Lifecycle Stage    : {document.lifecycle_stage}")

                print(f"Status             : {requirement.status}")

                print(f"Recommended Action : Complete verification and upload objective evidence.")

                print("-" * 80)

        print(f"\nOpen Gaps: {gaps}")