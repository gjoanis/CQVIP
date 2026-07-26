class TraceabilityEngine:
    """
    Builds a complete lifecycle Requirement Traceability Matrix (RTM).
    """

    DEFAULT_VERIFICATION = {

        "Planning & Requirements": "Review",

        "Design Qualification": "DQ",

        "Factory Acceptance Testing": "FAT",

        "Site Acceptance Testing": "SAT",

        "Engineering Studies": "Study",

        "Commissioning": "Commissioning",

        "Operational Readiness": "Review",

        "Installation Qualification": "IQ",

        "Operational Qualification": "OQ",

        "Performance Qualification": "PQ",

        "Continued Verification": "Periodic Review",

        "Retirement": "Decommissioning",

    }

    def __init__(self, requirements):

        self.requirements = requirements

    def recommended_phase(self, requirement):

        stage = getattr(
            requirement,
            "lifecycle_stage",
            None,
        )

        if stage:

            return self.DEFAULT_VERIFICATION.get(
                stage,
                "Review",
            )

        verification = getattr(
            requirement,
            "recommended_verification",
            None,
        )

        if verification:

            return verification

        return "Review"

    def build(self):

        matrix = []

        for requirement in self.requirements:

            matrix.append({

                "Requirement ID":
                    requirement.req_id,

                "Source Requirement":
                    getattr(
                        requirement,
                        "source_req_id",
                        requirement.req_id,
                    ),

                "System ID":
                    getattr(
                        requirement,
                        "system_id",
                        "",
                    ),

                "Document ID":
                    getattr(
                        requirement,
                        "document_id",
                        "",
                    ),

                "Document":
                    getattr(
                        requirement,
                        "document_name",
                        "",
                    ),

                "Document Type":
                    getattr(
                        requirement,
                        "document_type",
                        "",
                    ),

                "Lifecycle Stage":
                    getattr(
                        requirement,
                        "lifecycle_stage",
                        "",
                    ),

                "Requirement":
                    requirement.text,

                "Category":
                    getattr(
                        requirement,
                        "category",
                        "",
                    ),

                "Criticality":
                    getattr(
                        requirement,
                        "criticality",
                        "",
                    ),

                "Risk":
                    getattr(
                        requirement,
                        "risk",
                        "",
                    ),

                "Recommended Verification":
                    getattr(
                        requirement,
                        "recommended_verification",
                        "",
                    ),

                "Lifecycle Verification":
                    self.recommended_phase(
                        requirement,
                    ),

                "Protocol Section":
                    getattr(
                        requirement,
                        "protocol_section",
                        "",
                    ),

                "Suggested Test":
                    getattr(
                        requirement,
                        "suggested_test",
                        "",
                    ),

                "Acceptance Criteria":
                    getattr(
                        requirement,
                        "acceptance_criteria",
                        "",
                    ),

                "GMP Reference":
                    getattr(
                        requirement,
                        "gmp_reference",
                        "",
                    ),

                "Inspection Concern":
                    getattr(
                        requirement,
                        "inspection_concern",
                        "",
                    ),

                "Regulatory Rationale":
                    getattr(
                        requirement,
                        "regulatory_rationale",
                        "",
                    ),

                "Regulatory Sources":
                    getattr(
                        requirement,
                        "regulatory_sources",
                        [],
                    ),

                "Supporting Documents":
                    len(
                        getattr(
                            requirement,
                            "supporting_documents",
                            [],
                        )
                    ),

                "Status":
                    getattr(
                        requirement,
                        "status",
                        "",
                    ),

                "Verified":
                    getattr(
                        requirement,
                        "verified",
                        False,
                    ),

            })

        return matrix