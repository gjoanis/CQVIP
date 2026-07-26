from datetime import datetime
import uuid


class Evidence:
    """
    Represents objective evidence demonstrating that
    a requirement has been successfully verified.
    """

    def __init__(
        self,
        requirement_id,
        title,
        evidence_type,
        reference=None,
        description="",
        status="Pending",
    ):

        self.evidence_id = str(uuid.uuid4())

        self.requirement_id = requirement_id

        self.title = title

        self.evidence_type = evidence_type

        self.reference = reference

        self.description = description

        self.status = status

        self.created_at = datetime.utcnow()

        self.updated_at = datetime.utcnow()

    @property
    def verified(self):

        return self.status.lower() == "approved"

    def approve(self):

        self.status = "Approved"
        self.updated_at = datetime.utcnow()

    def reject(self):

        self.status = "Rejected"
        self.updated_at = datetime.utcnow()

    def mark_pending(self):

        self.status = "Pending"
        self.updated_at = datetime.utcnow()

    def to_dict(self):

        return {

            "evidence_id": self.evidence_id,

            "requirement_id": self.requirement_id,

            "title": self.title,

            "evidence_type": self.evidence_type,

            "reference": self.reference,

            "description": self.description,

            "status": self.status,

            "verified": self.verified,

            "created_at": self.created_at.isoformat(),

            "updated_at": self.updated_at.isoformat(),

        }