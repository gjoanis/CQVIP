from datetime import datetime

from app.database.database import get_connection
from app.models.document import Document


class DocumentRepository:

    @staticmethod
    def create(document):

        conn = get_connection()

        cursor = conn.execute(
            """
            INSERT INTO documents
            (
                system_id,
                lifecycle_stage_id,
                document_type_id,
                title,
                filename,
                original_filename,
                file_path,
                revision,
                document_number,
                description,
                status,
                effective_date,
                uploaded_by,
                uploaded_date,
                supersedes_document_id,
                is_current,
                ai_processed,
                ai_summary
            )

            VALUES
            (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            )
            """,
            (
                document.system_id,
                document.lifecycle_stage_id,
                document.document_type_id,
                document.title,
                document.filename,
                document.original_filename,
                document.file_path,
                document.revision,
                document.document_number,
                document.description,
                document.status,
                document.effective_date,
                document.uploaded_by,
                document.uploaded_date
                or datetime.now().isoformat(timespec="seconds"),
                document.supersedes_document_id,
                int(document.is_current),
                int(document.ai_processed),
                document.ai_summary,
            ),
        )

        document.id = cursor.lastrowid

        conn.commit()
        conn.close()

        return document

    @staticmethod
    def get(document_id):

        conn = get_connection()

        row = conn.execute(
            """
            SELECT *
            FROM documents
            WHERE id = ?
            """,
            (document_id,),
        ).fetchone()

        conn.close()

        if row is None:
            return None

        return DocumentRepository._build_document(row)

    @staticmethod
    def get_by_system(system_id):

        conn = get_connection()

        rows = conn.execute(
            """
            SELECT *
            FROM documents
            WHERE system_id = ?
            ORDER BY uploaded_date DESC
            """,
            (system_id,),
        ).fetchall()

        conn.close()

        return [
            DocumentRepository._build_document(row)
            for row in rows
        ]

    @staticmethod
    def get_by_stage(system_id, lifecycle_stage_id):

        conn = get_connection()

        rows = conn.execute(
            """
            SELECT *
            FROM documents
            WHERE system_id = ?
            AND lifecycle_stage_id = ?
            ORDER BY uploaded_date DESC
            """,
            (
                system_id,
                lifecycle_stage_id,
            ),
        ).fetchall()

        conn.close()

        return [
            DocumentRepository._build_document(row)
            for row in rows
        ]

    @staticmethod
    def update_ai_summary(document_id, summary):

        conn = get_connection()

        conn.execute(
            """
            UPDATE documents
            SET
                ai_processed = 1,
                ai_summary = ?
            WHERE id = ?
            """,
            (
                summary,
                document_id,
            ),
        )

        conn.commit()
        conn.close()

    @staticmethod
    def supersede(old_document_id, new_document_id):

        conn = get_connection()

        conn.execute(
            """
            UPDATE documents
            SET is_current = 0
            WHERE id = ?
            """,
            (old_document_id,),
        )

        conn.execute(
            """
            UPDATE documents
            SET supersedes_document_id = ?
            WHERE id = ?
            """,
            (
                old_document_id,
                new_document_id,
            ),
        )

        conn.commit()
        conn.close()

    @staticmethod
    def _build_document(row):

        document = Document(
            document_id=row["id"],
            system_id=row["system_id"],
            lifecycle_stage_id=row["lifecycle_stage_id"],
            document_type_id=row["document_type_id"],
            title=row["title"],
            filename=row["filename"],
            original_filename=row["original_filename"],
            file_path=row["file_path"],
            revision=row["revision"],
            document_number=row["document_number"],
            description=row["description"],
            status=row["status"],
            effective_date=row["effective_date"],
            uploaded_by=row["uploaded_by"],
            uploaded_date=row["uploaded_date"],
            supersedes_document_id=row["supersedes_document_id"],
        )

        document.is_current = bool(row["is_current"])
        document.ai_processed = bool(row["ai_processed"])
        document.ai_summary = row["ai_summary"]

        return document