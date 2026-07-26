class AIRequirementAnalyzer:

    def __init__(self):
        pass

    def build_default_analysis(
        self,
        requirement_text,
    ):

        text = requirement_text.lower()

        category = "Functional"
        criticality = "Medium"
        verification = "Test"
        risk = "Medium"
        protocol = "OQ"

        if (
            "hepa" in text
            or "particle" in text
            or "air change" in text
            or "hvac" in text
            or "temperature" in text
            or "humidity" in text
        ):

            category = "Environmental"
            criticality = "Critical"
            verification = "OQ"
            risk = "High"

        elif (
            "alarm" in text
            or "interlock" in text
            or "emergency" in text
        ):

            category = "Safety"
            criticality = "Critical"
            verification = "OQ"
            risk = "High"

        elif (
            "software" in text
            or "audit trail" in text
            or "part 11" in text
        ):

            category = "Computer System"
            criticality = "Critical"
            verification = "CSV"
            risk = "High"
            protocol = "CSV"

        return {

            "category": category,

            "criticality": criticality,

            "verification_strategy": verification,

            "risk": risk,

            "suggested_test": "Execute protocol and document objective evidence.",

            "inspection_concern": "Requirement should be traceable.",

            "gmp_reference": "EU GMP Annex 15",

            "acceptance_criteria": "Requirement demonstrated successfully.",

            "protocol_section": protocol,

            "regulatory_sources": [],

            "regulatory_rationale": "",

            "test_steps": [

                "Review requirement.",

                "Execute verification.",

                "Document results.",

            ],

            "objective_evidence": [

                "Executed protocol",

                "Approved results",

            ],

        }

    def analyze(
        self,
        requirement_text,
    ):

        return self.build_default_analysis(
            requirement_text
        )