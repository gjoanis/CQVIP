import sqlite3
from pathlib import Path

DB_FILE = Path("cqvip.db")

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def _add_missing_columns(conn, table_name, columns):

    existing_columns = {
        row["name"]
        for row in conn.execute(
            f"PRAGMA table_info({table_name})"
        ).fetchall()
    }

    for column_name, datatype in columns:

        if column_name not in existing_columns:

            conn.execute(
                f"""
                ALTER TABLE {table_name}
                ADD COLUMN {column_name} {datatype}
                """
            )


def _seed_lifecycle_stages(conn):

    stages = [
        (
            "Planning and Requirements",
            1,
            "Initial project planning, user requirements, specifications, and risk assessments.",
        ),
        (
            "Design Qualification",
            2,
            "Documented verification that the proposed design is suitable for its intended GMP use.",
        ),
        (
            "Factory Acceptance Testing",
            3,
            "Vendor-site testing performed before equipment or systems are shipped.",
        ),
        (
            "Site Acceptance Testing",
            4,
            "Site testing performed after delivery and installation.",
        ),
        (
            "Engineering Studies",
            5,
            "Engineering evaluations and studies performed before formal commissioning and qualification.",
        ),
        (
            "Commissioning",
            6,
            "Documented verification that the installed system operates according to approved design intent.",
        ),
        (
            "Operational Readiness",
            7,
            "Readiness activities required before qualification, including procedures, maintenance, calibration, and training.",
        ),
        (
            "Installation Qualification",
            8,
            "Documented verification that the system is installed according to approved specifications.",
        ),
        (
            "Operational Qualification",
            9,
            "Documented verification that the system operates throughout its intended operating ranges.",
        ),
        (
            "Performance Qualification",
            10,
            "Documented verification that the system consistently performs effectively under routine conditions.",
        ),
        (
            "Continued Verification",
            11,
            "Ongoing lifecycle oversight, periodic review, change control, CAPA, and requalification.",
        ),
        (
            "Retirement",
            12,
            "Controlled decommissioning, data retention, archival, and system retirement.",
        ),
    ]

    for name, sequence, description in stages:

        conn.execute(
            """
            INSERT OR IGNORE INTO lifecycle_stages
            (
                name,
                sequence,
                description,
                active
            )
            VALUES
            (
                ?, ?, ?, 1
            )
            """,
            (
                name,
                sequence,
                description,
            ),
        )


def _seed_document_types(conn):

    document_types = [
        (
            "Planning and Requirements",
            "User Requirements Specification",
            "URS",
            1,
        ),
        (
            "Planning and Requirements",
            "Functional Specification",
            "FS",
            0,
        ),
        (
            "Planning and Requirements",
            "Design Specification",
            "DS",
            0,
        ),
        (
            "Planning and Requirements",
            "Risk Assessment",
            "RA",
            1,
        ),
        (
            "Planning and Requirements",
            "Validation Plan",
            "VP",
            0,
        ),
        (
            "Design Qualification",
            "Design Qualification Protocol",
            "DQ",
            1,
        ),
        (
            "Design Qualification",
            "Design Qualification Report",
            "DQ Report",
            0,
        ),
        (
            "Factory Acceptance Testing",
            "Factory Acceptance Test Protocol",
            "FAT",
            0,
        ),
        (
            "Factory Acceptance Testing",
            "Factory Acceptance Test Report",
            "FAT Report",
            0,
        ),
        (
            "Site Acceptance Testing",
            "Site Acceptance Test Protocol",
            "SAT",
            0,
        ),
        (
            "Site Acceptance Testing",
            "Site Acceptance Test Report",
            "SAT Report",
            0,
        ),
        (
            "Engineering Studies",
            "Engineering Study Protocol",
            "Engineering Study",
            0,
        ),
        (
            "Engineering Studies",
            "Engineering Study Report",
            "Engineering Study Report",
            0,
        ),
        (
            "Commissioning",
            "Commissioning Plan",
            "Commissioning Plan",
            1,
        ),
        (
            "Commissioning",
            "Commissioning Protocol",
            "Commissioning Protocol",
            1,
        ),
        (
            "Commissioning",
            "Commissioning Test Script",
            "Commissioning Test",
            0,
        ),
        (
            "Commissioning",
            "Commissioning Summary Report",
            "Commissioning Report",
            1,
        ),
        (
            "Operational Readiness",
            "Standard Operating Procedure",
            "SOP",
            1,
        ),
        (
            "Operational Readiness",
            "Work Instruction",
            "WI",
            0,
        ),
        (
            "Operational Readiness",
            "Preventive Maintenance Procedure",
            "PM",
            1,
        ),
        (
            "Operational Readiness",
            "Calibration Procedure",
            "Calibration",
            0,
        ),
        (
            "Operational Readiness",
            "Training Record",
            "Training",
            0,
        ),
        (
            "Operational Readiness",
            "Spare Parts List",
            "Spare Parts",
            0,
        ),
        (
            "Installation Qualification",
            "Installation Qualification Protocol",
            "IQ",
            1,
        ),
        (
            "Installation Qualification",
            "Installation Qualification Report",
            "IQ Report",
            0,
        ),
        (
            "Operational Qualification",
            "Operational Qualification Protocol",
            "OQ",
            1,
        ),
        (
            "Operational Qualification",
            "Operational Qualification Report",
            "OQ Report",
            0,
        ),
        (
            "Performance Qualification",
            "Performance Qualification Protocol",
            "PQ",
            1,
        ),
        (
            "Performance Qualification",
            "Performance Qualification Report",
            "PQ Report",
            0,
        ),
        (
            "Continued Verification",
            "Periodic Review",
            "Periodic Review",
            0,
        ),
        (
            "Continued Verification",
            "Change Control",
            "Change Control",
            0,
        ),
        (
            "Continued Verification",
            "Deviation",
            "Deviation",
            0,
        ),
        (
            "Continued Verification",
            "Corrective and Preventive Action",
            "CAPA",
            0,
        ),
        (
            "Continued Verification",
            "Requalification Protocol",
            "Requalification",
            0,
        ),
        (
            "Retirement",
            "Decommissioning Plan",
            "Decommissioning Plan",
            0,
        ),
        (
            "Retirement",
            "Decommissioning Report",
            "Decommissioning Report",
            0,
        ),
    ]

    for stage_name, name, code, required_default in document_types:

        stage = conn.execute(
            """
            SELECT id
            FROM lifecycle_stages
            WHERE name = ?
            """,
            (stage_name,),
        ).fetchone()

        if not stage:
            continue

        conn.execute(
            """
            INSERT OR IGNORE INTO document_types
            (
                lifecycle_stage_id,
                name,
                code,
                required_default,
                active
            )
            VALUES
            (
                ?, ?, ?, ?, 1
            )
            """,
            (
                stage["id"],
                name,
                code,
                required_default,
            ),
        )


def initialize_database():

    conn = get_connection()

    try:

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS facilities
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                description TEXT,

                created_date TEXT
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projects
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                facility_id INTEGER NOT NULL,

                name TEXT NOT NULL,

                description TEXT,

                created_date TEXT,

                FOREIGN KEY(facility_id)
                    REFERENCES facilities(id)
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS systems
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                project_id INTEGER NOT NULL,

                name TEXT NOT NULL,

                description TEXT,

                created_date TEXT,

                FOREIGN KEY(project_id)
                    REFERENCES projects(id)
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS lifecycle_stages
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL UNIQUE,

                sequence INTEGER NOT NULL UNIQUE,

                description TEXT,

                active INTEGER NOT NULL DEFAULT 1
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS document_types
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                lifecycle_stage_id INTEGER NOT NULL,

                name TEXT NOT NULL,

                code TEXT NOT NULL,

                description TEXT,

                required_default INTEGER NOT NULL DEFAULT 0,

                active INTEGER NOT NULL DEFAULT 1,

                UNIQUE(lifecycle_stage_id, name),

                FOREIGN KEY(lifecycle_stage_id)
                    REFERENCES lifecycle_stages(id)
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                system_id INTEGER NOT NULL,

                lifecycle_stage_id INTEGER NOT NULL,

                document_type_id INTEGER NOT NULL,

                title TEXT,

                filename TEXT NOT NULL,

                original_filename TEXT,

                file_path TEXT NOT NULL,

                revision TEXT,

                document_number TEXT,

                description TEXT,

                status TEXT NOT NULL DEFAULT 'Draft',

                effective_date TEXT,

                uploaded_by TEXT,

                uploaded_date TEXT,

                supersedes_document_id INTEGER,

                is_current INTEGER NOT NULL DEFAULT 1,

                ai_processed INTEGER NOT NULL DEFAULT 0,

                ai_summary TEXT,

                FOREIGN KEY(system_id)
                    REFERENCES systems(id),

                FOREIGN KEY(lifecycle_stage_id)
                    REFERENCES lifecycle_stages(id),

                FOREIGN KEY(document_type_id)
                    REFERENCES document_types(id),

                FOREIGN KEY(supersedes_document_id)
                    REFERENCES documents(id)
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS requirements
            (
                req_id TEXT PRIMARY KEY,

                source_req_id TEXT,

                system_id INTEGER,

                document_id INTEGER,

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

                na_date TEXT,

                ai_processed INTEGER DEFAULT 0,

                ai_summary TEXT,

                FOREIGN KEY(system_id)
                    REFERENCES systems(id),

                FOREIGN KEY(document_id)
                    REFERENCES documents(id)
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS supporting_documents
            (
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

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS evidence
            (
                evidence_id TEXT PRIMARY KEY,

                requirement_id TEXT NOT NULL,

                title TEXT NOT NULL,

                evidence_type TEXT NOT NULL,

                reference TEXT,

                description TEXT,

                status TEXT NOT NULL DEFAULT 'Pending',

                created_at TEXT,

                updated_at TEXT,

                FOREIGN KEY(requirement_id)
                    REFERENCES requirements(req_id)
            )
            """
        )

        _add_missing_columns(
            conn,
            "requirements",
            [
                ("source_req_id", "TEXT"),
                ("system_id", "INTEGER"),
                ("document_id", "INTEGER"),
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
            ],
        )

        conn.execute(
            """
            UPDATE requirements
            SET source_req_id = req_id
            WHERE source_req_id IS NULL
               OR TRIM(source_req_id) = ''
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_projects_facility_id
            ON projects(facility_id)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_systems_project_id
            ON systems(project_id)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_documents_system_id
            ON documents(system_id)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_documents_stage_id
            ON documents(lifecycle_stage_id)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_documents_type_id
            ON documents(document_type_id)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_requirements_system_id
            ON requirements(system_id)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_requirements_document_id
            ON requirements(document_id)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_requirements_source_req_id
            ON requirements(source_req_id)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_evidence_requirement_id
            ON evidence(requirement_id)
            """
        )

        _seed_lifecycle_stages(conn)
        _seed_document_types(conn)

        conn.commit()

    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()