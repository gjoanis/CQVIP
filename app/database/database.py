import sqlite3
from pathlib import Path

DB_FILE = Path("cqvip.db")


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():

    conn = get_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS requirements (

            req_id TEXT PRIMARY KEY,

            text TEXT,

            category TEXT,

            criticality TEXT,

            verification TEXT,

            status TEXT,

            disposition TEXT,

            verified INTEGER,

            risk TEXT,

            gmp_reference TEXT,

            acceptance_criteria TEXT,

            suggested_test TEXT,

            inspection_concern TEXT,

            protocol_section TEXT,

            assigned_to TEXT,

            assigned_date TEXT,

            review_date TEXT,

            verified_by TEXT,

            approved_by TEXT,

            closed_date TEXT,

            comments TEXT,

            na_reason TEXT,

            na_justification TEXT,

            na_approved_by TEXT,

            na_date TEXT

        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS supporting_documents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            requirement_id TEXT NOT NULL,

            filename TEXT NOT NULL,

            document_type TEXT NOT NULL,

            file_path TEXT NOT NULL,

            uploaded_by TEXT,

            upload_date TEXT,

            ai_processed INTEGER DEFAULT 0,

            ai_summary TEXT,

            FOREIGN KEY(requirement_id)
                REFERENCES requirements(req_id)

        )
        """
    )

    columns = [
        ("assigned_to", "TEXT"),
        ("assigned_date", "TEXT"),
        ("review_date", "TEXT"),
        ("verified_by", "TEXT"),
        ("approved_by", "TEXT"),
        ("closed_date", "TEXT"),
        ("comments", "TEXT"),
        ("disposition", "TEXT"),
        ("na_reason", "TEXT"),
        ("na_justification", "TEXT"),
        ("na_approved_by", "TEXT"),
        ("na_date", "TEXT"),
        ("ai_processed", "INTEGER DEFAULT 0"),
        ("ai_summary", "TEXT"),
    ]

    existing = {
        row["name"]
        for row in conn.execute(
            "PRAGMA table_info(requirements)"
        )
    }

    for name, datatype in columns:

        if name not in existing:

            conn.execute(
                f"ALTER TABLE requirements ADD COLUMN {name} {datatype}"
            )

    conn.commit()
    conn.close()