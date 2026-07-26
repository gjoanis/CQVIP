from app.models.evidence import Evidence


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
    Represents a lifecycle requirement.
    """

    def __init__(
        self,
        req_id,
        system_id,
        text,
        category,
        document_id=None,
        source_req_id=None,
    ):

        # Identity

        self.req_id = req_id
        self.source_req_id = source_req_id or req_id

        # Hierarchy

        self.system_id = system_id
        self.document_id = document_id

        self.lifecycle_stage = None
        self.document_type = None
        self.document_name = None

        # Requirement

        self.text = text
        self.category = category

        # AI Classification

        self.criticality = None
        self.recommended_verification = None
        self.risk = None
        self.gmp_reference = None
        self.acceptance_criteria = None
        self.suggested_test = None
        self.inspection_concern = None
        self.protocol_section = None

        self.regulatory_rationale = None
        self.regulatory_sources = []

        self.test_steps = []

        # Evidence

        self.evidence = []
        self.objective_evidence = []

        # Workflow

        self.status = "Open"
        self.disposition = "Applicable"

        self.assigned_to = None
        self.assigned_date = None
        self.review_date = None

        self.verified = False
        self.verified_by = None

        self.approved_by = None
        self.closed_date = None
        self.comments = None

        # Not Applicable

        self.na_reason = None
        self.na_justification = None
        self.na_approved_by = None
        self.na_date = None

        # Supporting Evidence

        self.supporting_documents = []

        # Traceability

        self.links = VerificationLink(req_id)

        self.lifecycle_tests = {

            "Planning": [],

            "URS": [],

            "FRS": [],

            "DS": [],

            "DQ": [],

            "FAT": [],

            "SAT": [],

            "Commissioning": [],

            "IQ": [],

            "OQ": [],

            "PQ": [],

            "CPV": [],

        }

    def mark_verified(self, test_id):

        self.verified = True
        self.verified_by = test_id

        self.links.add_test(test_id)

    def add_trace_link(self, test_id):

        self.links.add_test(test_id)

    def add_lifecycle_test(
        self,
        phase,
        test_id,
    ):

        if phase not in self.lifecycle_tests:

            self.lifecycle_tests[phase] = []

        self.lifecycle_tests[phase].append(test_id)

        self.links.add_test(test_id)

    def add_evidence(self, evidence):

        if not isinstance(evidence, Evidence):

            raise TypeError(
                "evidence must be an Evidence object"
            )

        self.evidence.append(evidence)

        if evidence.verified:

            self.verified = True

    def remove_evidence(self, evidence_id):

        self.evidence = [

            e

            for e in self.evidence

            if e.evidence_id != evidence_id

        ]

        self.verified = any(

            e.verified

            for e in self.evidence

        )

    def approved_evidence(self):

        return [

            e

            for e in self.evidence

            if e.verified

        ]

    def set_recommended_verification(
        self,
        verification,
    ):

        self.recommended_verification = verification

    def set_criticality(
        self,
        criticality,
    ):

        self.criticality = criticality

    def to_dict(self):

        return {

            "req_id": self.req_id,

            "system_id": self.system_id,

            "document_id": self.document_id,

            "text": self.text,

            "category": self.category,

            "criticality": self.criticality,

            "recommended_verification": self.recommended_verification,

            "risk": self.risk,

            "verified": self.verified,

            "status": self.status,

            "evidence_count": len(self.evidence),

            "approved_evidence": len(self.approved_evidence()),

        }