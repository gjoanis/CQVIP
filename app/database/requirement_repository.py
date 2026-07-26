from datetime import datetime

from app.database.database import get_connection
from app.models.requirement import Requirement
from app.repositories.evidence_repository import EvidenceRepository


class RequirementRepository:

    @staticmethod
    def save(requirement):

        conn = get_connection()

        conn.execute(
            """
            INSERT OR REPLACE INTO requirements
            (
                req_id,
                source_req_id,
                system_id,
                document_id,
                text,
                category,
                criticality,
                verification,
                status,
                disposition,
                verified,
                risk,
                gmp_reference,
                acceptance_criteria,
                suggested_test,
                inspection_concern,
                protocol_section,
                assigned_to,
                assigned_date,
                review_date,
                verified_by,
                approved_by,
                closed_date,
                comments,
                na_reason,
                na_justification,
                na_approved_by,
                na_date,
                ai_processed,
                ai_summary
            )

            VALUES
            (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            )
            """,
            (
                requirement.req_id,
                getattr(requirement, "source_req_id", requirement.req_id),
                requirement.system_id,
                getattr(requirement, "document_id", None),
                requirement.text,
                requirement.category,
                requirement.criticality,
                requirement.recommended_verification,
                getattr(requirement, "status", "Open"),
                getattr(requirement, "disposition", "Applicable"),
                int(getattr(requirement, "verified", False)),
                requirement.risk,
                requirement.gmp_reference,
                requirement.acceptance_criteria,
                requirement.suggested_test,
                requirement.inspection_concern,
                requirement.protocol_section,
                getattr(requirement, "assigned_to", None),
                getattr(requirement, "assigned_date", None),
                getattr(requirement, "review_date", None),
                getattr(requirement, "verified_by", None),
                getattr(requirement, "approved_by", None),
                getattr(requirement, "closed_date", None),
                getattr(requirement, "comments", None),
                getattr(requirement, "na_reason", None),
                getattr(requirement, "na_justification", None),
                getattr(requirement, "na_approved_by", None),
                getattr(requirement, "na_date", None),
                1,
                getattr(requirement, "regulatory_rationale", None),
            ),
        )

        for evidence in getattr(requirement, "evidence", []):
            EvidenceRepository.save(evidence)

        conn.commit()
        conn.close()

    @staticmethod
    def _build_requirement(row):

        req = Requirement(
            req_id=row["req_id"],
            source_req_id=row["source_req_id"],
            system_id=row["system_id"],
            document_id=row["document_id"],
            text=row["text"],
            category=row["category"],
        )

        req.criticality = row["criticality"]
        req.recommended_verification = row["verification"]
        req.status = row["status"]
        req.disposition = row["disposition"] or "Applicable"
        req.verified = bool(row["verified"])

        req.risk = row["risk"]
        req.gmp_reference = row["gmp_reference"]
        req.acceptance_criteria = row["acceptance_criteria"]
        req.suggested_test = row["suggested_test"]
        req.inspection_concern = row["inspection_concern"]
        req.protocol_section = row["protocol_section"]

        req.assigned_to = row["assigned_to"]
        req.assigned_date = row["assigned_date"]
        req.review_date = row["review_date"]
        req.verified_by = row["verified_by"]
        req.approved_by = row["approved_by"]
        req.closed_date = row["closed_date"]
        req.comments = row["comments"]

        req.na_reason = row["na_reason"]
        req.na_justification = row["na_justification"]
        req.na_approved_by = row["na_approved_by"]
        req.na_date = row["na_date"]

        req.regulatory_rationale = row["ai_summary"]

        req.evidence = EvidenceRepository.by_requirement(
            req.req_id
        )

        req.verified = any(
            evidence.verified
            for evidence in req.evidence
        ) or req.verified

        return req

    @staticmethod
    def all():

        conn = get_connection()

        rows = conn.execute(
            """
            SELECT *
            FROM requirements
            ORDER BY req_id
            """
        ).fetchall()

        conn.close()

        return [
            RequirementRepository._build_requirement(row)
            for row in rows
        ]

    @staticmethod
    def get(req_id: str):

        conn = get_connection()

        row = conn.execute(
            """
            SELECT *
            FROM requirements
            WHERE req_id = ?
            """,
            (req_id,),
        ).fetchone()

        conn.close()

        if row is None:
            return None

        return RequirementRepository._build_requirement(row)

    @staticmethod
    def update_status(req_id, status):

        conn = get_connection()

        now = datetime.now().isoformat(timespec="seconds")

        assigned_date = None
        review_date = None
        closed_date = None

        if status == "Assigned":
            assigned_date = now

        elif status == "Under Review":
            review_date = now

        elif status == "Closed":
            closed_date = now

        conn.execute(
            """
            UPDATE requirements
            SET
                status = ?,
                verified = ?,
                assigned_date = COALESCE(?, assigned_date),
                review_date = COALESCE(?, review_date),
                closed_date = COALESCE(?, closed_date)
            WHERE req_id = ?
            """,
            (
                status,
                1 if status == "Verified" else 0,
                assigned_date,
                review_date,
                closed_date,
                req_id,
            ),
        )

        conn.commit()
        conn.close()

    @staticmethod
    def assign_owner(req_id, assigned_to):

        conn = get_connection()

        now = datetime.now().isoformat(timespec="seconds")

        conn.execute(
            """
            UPDATE requirements
            SET
                assigned_to = ?,
                assigned_date = ?,
                status = ?
            WHERE req_id = ?
            """,
            (
                assigned_to,
                now,
                "Assigned",
                req_id,
            ),
        )

        conn.commit()
        conn.close()

    @staticmethod
    def mark_not_applicable(
        req_id,
        reason,
        justification,
        approved_by,
    ):

        conn = get_connection()

        now = datetime.now().isoformat(timespec="seconds")

        conn.execute(
            """
            UPDATE requirements
            SET
                disposition = ?,
                status = ?,
                na_reason = ?,
                na_justification = ?,
                na_approved_by = ?,
                na_date = ?
            WHERE req_id = ?
            """,
            (
                "Not Applicable",
                "Closed",
                reason,
                justification,
                approved_by,
                now,
                req_id,
            ),
        )

        conn.commit()
        conn.close()