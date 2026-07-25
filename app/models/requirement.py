class VerificationLink:
    """
    Stores traceability links between a requirement and lifecycle tests.
    """

    def __init__(self, requirement_id):
        self.requirement_id = requirement_id
        self.tests = []

    def add_test(self, test_id):
        self.tests.append(test_id)


class Requirement:
    """
    Represents a single requirement extracted from a CQV document.
    """

    def __init__(self, req_id, text, category):
        self.req_id = req_id
        self.text = text
        self.category = category

        self.criticality = None
        self.verified = False
        self.verified_by = None

        # Workflow Status
        self.status = "Open"

        # Business Disposition
        self.disposition = "Applicable"

        # Assignment / Workflow
        self.assigned_to = None
        self.assigned_date = None
        self.review_date = None
        self.approved_by = None
        self.closed_date = None
        self.comments = None

        # Applicability
        self.na_reason = None
        self.na_justification = None
        self.na_approved_by = None
        self.na_date = None

        # AI Generated Content
        self.recommended_verification = None
        self.risk = None
        self.gmp_reference = None
        self.acceptance_criteria = None
        self.suggested_test = None
        self.inspection_concern = None
        self.protocol_section = None
        self.regulatory_rationale = None

        # Evidence / Supporting Documentation
        self.supporting_documents = []

        # Generated Content
        self.test_steps = []
        self.objective_evidence = []
        self.regulatory_sources = []

        self.links = VerificationLink(req_id)

        self.lifecycle_tests = {
            "DQ": [],
            "FAT": [],
            "SAT": [],
            "Commissioning": [],
            "IQ": [],
            "OQ": [],
            "PQ": []
        }

    def mark_verified(self, test_id):
        self.verified = True
        self.verified_by = test_id
        self.links.add_test(test_id)

    def add_trace_link(self, test_id):
        self.links.add_test(test_id)

    def add_lifecycle_test(self, phase, test_id):
        if phase not in self.lifecycle_tests:
            self.lifecycle_tests[phase] = []

        self.lifecycle_tests[phase].append(test_id)
        self.links.add_test(test_id)

    def set_recommended_verification(self, verification):
        self.recommended_verification = verification

    def set_criticality(self, criticality):
        self.criticality = criticality