from app.database.database import get_connection


class SystemRepository:

    @staticmethod
    def get_or_create(facility_name, project_name, system_name):

        conn = get_connection()

        facility = conn.execute(
            """
            SELECT id
            FROM facilities
            WHERE name = ?
            """,
            (facility_name,),
        ).fetchone()

        if facility:

            facility_id = facility["id"]

        else:

            cursor = conn.execute(
                """
                INSERT INTO facilities
                (
                    name
                )
                VALUES
                (
                    ?
                )
                """,
                (facility_name,),
            )

            facility_id = cursor.lastrowid

        project = conn.execute(
            """
            SELECT id
            FROM projects
            WHERE
                facility_id = ?
                AND name = ?
            """,
            (
                facility_id,
                project_name,
            ),
        ).fetchone()

        if project:

            project_id = project["id"]

        else:

            cursor = conn.execute(
                """
                INSERT INTO projects
                (
                    facility_id,
                    name
                )
                VALUES
                (
                    ?,
                    ?
                )
                """,
                (
                    facility_id,
                    project_name,
                ),
            )

            project_id = cursor.lastrowid

        system = conn.execute(
            """
            SELECT id
            FROM systems
            WHERE
                project_id = ?
                AND name = ?
            """,
            (
                project_id,
                system_name,
            ),
        ).fetchone()

        if system:

            system_id = system["id"]

        else:

            cursor = conn.execute(
                """
                INSERT INTO systems
                (
                    project_id,
                    name
                )
                VALUES
                (
                    ?,
                    ?
                )
                """,
                (
                    project_id,
                    system_name,
                ),
            )

            system_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return system_id