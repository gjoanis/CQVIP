from app.database.database import get_connection
from app.models.evidence import Evidence


class EvidenceRepository:

    @staticmethod
    def save(evidence):

        conn = get_connection()

        conn.execute(
            """
            INSERT OR REPLACE INTO evidence
            (
                evidence_id,
                requirement_id,
                title,
                evidence_type,
                reference,
                description,
                status,
                created_at,
                updated_at
            )
            VALUES
            (
                ?,?,?,?,?,?,?,?,?
            )
            """,
            (
                evidence.evidence_id,
                evidence.requirement_id,
                evidence.title,
                evidence.evidence_type,
                evidence.reference,
                evidence.description,
                evidence.status,
                evidence.created_at.isoformat(),
                evidence.updated_at.isoformat(),
            ),
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get(evidence_id):

        conn = get_connection()

        row = conn.execute(
            """
            SELECT *
            FROM evidence
            WHERE evidence_id = ?
            """,
            (evidence_id,),
        ).fetchone()

        conn.close()

        if row is None:
            return None

        evidence = Evidence(
            requirement_id=row["requirement_id"],
            title=row["title"],
            evidence_type=row["evidence_type"],
            reference=row["reference"],
            description=row["description"],
            status=row["status"],
        )

        evidence.evidence_id = row["evidence_id"]

        return evidence

    @staticmethod
    def by_requirement(requirement_id):

        conn = get_connection()

        rows = conn.execute(
            """
            SELECT *
            FROM evidence
            WHERE requirement_id = ?
            ORDER BY created_at
            """,
            (requirement_id,),
        ).fetchall()

        conn.close()

        evidence_list = []

        for row in rows:

            evidence = Evidence(
                requirement_id=row["requirement_id"],
                title=row["title"],
                evidence_type=row["evidence_type"],
                reference=row["reference"],
                description=row["description"],
                status=row["status"],
            )

            evidence.evidence_id = row["evidence_id"]

            evidence_list.append(evidence)

        return evidence_list

    @staticmethod
    def update_status(evidence_id, status):

        conn = get_connection()

        conn.execute(
            """
            UPDATE evidence
            SET
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE evidence_id = ?
            """,
            (
                status,
                evidence_id,
            ),
        )

        conn.commit()
        conn.close()

    @staticmethod
    def delete(evidence_id):

        conn = get_connection()

        conn.execute(
            """
            DELETE FROM evidence
            WHERE evidence_id = ?
            """,
            (evidence_id,),
        )

        conn.commit()
        conn.close()