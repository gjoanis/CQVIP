class VerificationStrategy:
    """
    Builds a lifecycle verification strategy for a requirement.
    """

    def build(self, requirement):

        strategy = {
            "dq": [],
            "fat": [],
            "sat": [],
            "commissioning": [],
            "iq": [],
            "oq": [],
            "pq": []
        }

        text = (
            (requirement.text or "") + " " +
            (requirement.category or "") + " " +
            (requirement.suggested_test or "") + " " +
            (requirement.acceptance_criteria or "")
        ).lower()

        is_facility = any(word in text for word in [
            "room", "wall", "ceiling", "floor", "door", "cleanroom",
            "airlock", "layout", "coving", "surface", "fixture"
        ])

        is_utility = any(word in text for word in [
            "purified water", "pou", "utility", "electricity",
            "electrical", "compressed air", "steam", "gas"
        ])

        is_environmental = any(word in text for word in [
            "temperature", "humidity", "pressure", "airflow",
            "air changes", "particle", "environmental", "monitoring"
        ])

        is_cleaning = any(word in text for word in [
            "cleaning", "cleanable", "sanitize", "sanitizing",
            "microbial", "bioburden", "endotoxin", "residue"
        ])

        is_control = any(word in text for word in [
            "alarm", "interlock", "access control", "software",
            "electronic record", "audit trail", "monitoring instrument"
        ])

        # DQ
        if is_facility or is_utility or is_environmental or is_control:
            strategy["dq"].append(
                "Verify the design meets the URS, GMP impact, and approved engineering specifications."
            )

        # FAT
        if is_control or is_utility:
            strategy["fat"].append(
                "Verify key functions, alarms, controls, and vendor testing before shipment where applicable."
            )

        # SAT
        if is_control or is_utility or is_environmental:
            strategy["sat"].append(
                "Verify field installation, interfaces, and site integration after delivery."
            )

        # Commissioning
        if is_facility or is_utility or is_environmental or is_control:
            strategy["commissioning"].append(
                "Verify startup, calibration, functional checks, and readiness for qualification."
            )

        # IQ
        if is_facility or is_utility or is_control:
            strategy["iq"].append(
                "Verify installation against drawings, specifications, components, materials, and calibration requirements."
            )

        # OQ
        if is_environmental or is_control or is_utility:
            strategy["oq"].append(
                "Challenge operation, alarms, limits, controls, and worst-case conditions."
            )

        # PQ
        if is_cleaning or is_environmental or is_utility:
            strategy["pq"].append(
                "Verify sustained performance during routine or simulated operational conditions."
            )

        # Default fallback
        if not any(strategy.values()):
            strategy["commissioning"].append(
                "Verify the requirement through documented commissioning or qualification evidence."
            )

        return strategy