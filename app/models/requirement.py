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
        self.recommended_verification = None
        self.links = VerificationLink(req_id)

    def mark_verified(self, test_id):
        self.verified = True
        self.verified_by = test_id
        self.links.add_test(test_id)

    def add_trace_link(self, test_id):
        self.links.add_test(test_id)

    def set_recommended_verification(self, verification):
        self.recommended_verification = verification

    def set_criticality(self, criticality):
        self.criticality = criticality