class InspectionService:
    """
    Evaluates inspection readiness for the lifecycle-based CQVIP model.
    """

    def __init__(self, asset):

        self.asset = asset

    def check_readiness(self):

        total_requirements = 0

        verified_requirements = 0

        open_requirements = 0

        open_critical = 0

        missing_evidence = 0

        lifecycle_gaps = 0

        for document in self.asset.documents:

            for requirement in document.requirements:

                total_requirements += 1

                if getattr(requirement, "verified", False):

                    verified_requirements += 1

                else:

                    open_requirements += 1

                    if getattr(requirement, "criticality", "") == "Critical":

                        open_critical += 1

                if len(getattr(requirement, "supporting_documents", [])) == 0:

                    missing_evidence += 1

                if not getattr(requirement, "lifecycle_stage", ""):

                    lifecycle_gaps += 1

        ready = (

            open_requirements == 0

            and open_critical == 0

            and lifecycle_gaps == 0

        )

        print("\nINSPECTION READINESS")
        print("-" * 50)

        print("Asset:", self.asset.name)

        print("Total Requirements:", total_requirements)

        print("Verified:", verified_requirements)

        print("Open Requirements:", open_requirements)

        print("Open Critical Requirements:", open_critical)

        print("Missing Evidence:", missing_evidence)

        print("Lifecycle Gaps:", lifecycle_gaps)

        if ready:

            print("Status: Inspection Ready")

        else:

            print("Status: Inspection NOT Ready")

        return {

            "ready": ready,

            "total_requirements": total_requirements,

            "verified_requirements": verified_requirements,

            "open_requirements": open_requirements,

            "open_critical": open_critical,

            "missing_evidence": missing_evidence,

            "lifecycle_gaps": lifecycle_gaps,

        }