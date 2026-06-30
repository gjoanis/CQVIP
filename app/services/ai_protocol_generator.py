from datetime import datetime


class AIProtocolGenerator:
    """
    Generates protocol content from AI-enriched requirements.
    """

    def __init__(self, requirements):
        self.requirements = requirements

    def generate(self):

        protocol = []

        protocol.append({
            "title": "Protocol Information",
            "document_number": "AUTO-GEN",
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        for req in self.requirements:

            protocol.append({

                "requirement_id":
                    getattr(req, "req_id", ""),

                "requirement":
                    getattr(req, "text", ""),

                "category":
                    getattr(req, "category", ""),

                "criticality":
                    getattr(req, "criticality", ""),

                "verification":
                    getattr(
                        req,
                        "recommended_verification",
                        ""
                    ),

                "objective":
                    f"Verify requirement {getattr(req,'req_id','')} is satisfied.",

                "test_steps":
                    getattr(
                        req,
                        "test_steps",
                        []
                    ),

                "acceptance_criteria":
                    getattr(
                        req,
                        "acceptance_criteria",
                        ""
                    ),

                "objective_evidence":
                    getattr(
                        req,
                        "objective_evidence",
                        []
                    ),

                "gmp_reference":
                    getattr(
                        req,
                        "gmp_reference",
                        ""
                    ),

                "risk":
                    getattr(
                        req,
                        "risk",
                        ""
                    )

            })

        return protocol

    def by_phase(self, phase):

        protocols = []

        for req in self.requirements:

            verification = getattr(
                req,
                "recommended_verification",
                ""
            ).upper()

            if phase.upper() in verification:

                protocols.append(req)

        return AIProtocolGenerator(protocols).generate()