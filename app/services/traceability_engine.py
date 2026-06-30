class TraceabilityEngine:
    """
    Creates a Requirement Traceability Matrix (RTM)
    linking URS requirements to lifecycle verification.
    """

    DEFAULT_PHASES = {
        "Environmental Control": "OQ",
        "Utilities": "IQ",
        "Equipment": "IQ",
        "Automation": "OQ",
        "Software": "CSV",
        "Documentation": "Review",
        "Safety": "IQ",
        "Cleaning": "OQ",
        "Process": "PQ",
        "General": "IQ",
    }

    def __init__(self, requirements):
        self.requirements = requirements

    def recommended_phase(self, requirement):

        category = getattr(
            requirement,
            "category",
            "General"
        )

        return self.DEFAULT_PHASES.get(
            category,
            "IQ"
        )

    def build(self):

        matrix = []

        for requirement in self.requirements:

            matrix.append({

                "Requirement ID":
                    getattr(requirement, "req_id", ""),

                "Requirement":
                    getattr(requirement, "text", ""),

                "Category":
                    getattr(requirement, "category", ""),

                "Criticality":
                    getattr(requirement, "criticality", ""),

                "Verification":
                    getattr(
                        requirement,
                        "recommended_verification",
                        ""
                    ),

                "Suggested Test":
                    getattr(
                        requirement,
                        "suggested_test",
                        ""
                    ),

                "Lifecycle Phase":
                    self.recommended_phase(
                        requirement
                    ),

                "Acceptance Criteria":
                    getattr(
                        requirement,
                        "acceptance_criteria",
                        ""
                    ),

                "GMP Reference":
                    getattr(
                        requirement,
                        "gmp_reference",
                        ""
                    ),

                "Verified":
                    getattr(
                        requirement,
                        "verified",
                        False
                    )

            })

        return matrix