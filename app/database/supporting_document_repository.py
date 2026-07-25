from datetime import datetime

from app.database.database import get_connection


class SupportingDocumentRepository:

    @staticmethod
    def save(
        requirement_id,
        filename,
        document_type,
        file_path,
        uploaded_by="System",
        ai_processed=False,
        ai_summary="",
    ):

        conn = get_connection()

        conn.execute(
            """
            INSERT INTO supporting_documents
            (
                requirement_id,
                filename,
                document_type,
                file_path,
                uploaded_by,
                upload_date,
                ai_processed,
                ai_summary
            )

            VALUES
            (
                ?,?,?,?,?,?,?,?
            )
            """,
            (
                requirement_id,
                filename,
                document_type,
                file_path,
                uploaded_by,
                datetime.now().isoformat(timespec="seconds"),
                ai_processed,
                ai_summary,
            ),
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_for_requirement(requirement_id):

        conn = get_connection()

        rows = conn.execute(
            """
            SELECT *
            FROM supporting_documents
            WHERE requirement_id = ?
            ORDER BY upload_date DESC
            """,
            (requirement_id,),
        ).fetchall()

        conn.close()

        return rows

    @staticmethod
    def delete(document_id):

        conn = get_connection()

        conn.execute(
            """
            DELETE
            FROM supporting_documents
            WHERE id = ?
            """,
            (document_id,),
        )

        conn.commit()
        conn.close()