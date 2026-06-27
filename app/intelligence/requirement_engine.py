class RequirementEngine:
    """
    Converts a requirement into a structured
    validation strategy.
    """

    def analyze(self, requirement):

        text = requirement.text.lower()

        strategy = {
            "objective": "",
            "procedure": [],
            "acceptance": [],
            "evidence": [],
            "phase": requirement.recommended_verification
        }

        if "alarm" in text:

            strategy["objective"] = (
                "Verify the alarm activates under the required condition."
            )

            strategy["procedure"] = [
                "Configure the system for normal operation.",
                "Create the specified alarm condition.",
                "Verify the alarm activates.",
                "Verify acknowledgement and recovery."
            ]

            strategy["acceptance"] = [
                "Alarm activates correctly.",
                "Alarm is logged.",
                "System recovers after acknowledgement."
            ]

            strategy["evidence"] = [
                "Alarm screenshots",
                "Audit trail",
                "Alarm history"
            ]

        elif "temperature" in text:

            strategy["objective"] = (
                "Verify temperature remains within specification."
            )

            strategy["procedure"] = [
                "Connect calibrated temperature instrument.",
                "Execute operating cycle.",
                "Record temperature.",
                "Compare to specification."
            ]

            strategy["acceptance"] = [
                "Temperature remains within specification."
            ]

            strategy["evidence"] = [
                "Temperature log",
                "Calibration certificate"
            ]

        elif "pressure" in text:

            strategy["objective"] = (
                "Verify pressure remains within specification."
            )

            strategy["procedure"] = [
                "Connect calibrated pressure gauge.",
                "Run operating cycle.",
                "Record pressure.",
                "Compare against URS."
            ]

            strategy["acceptance"] = [
                "Pressure remains within specification."
            ]

            strategy["evidence"] = [
                "Pressure trend",
                "Calibration record"
            ]

        else:

            strategy["objective"] = (
                "Verify the requirement is satisfied."
            )

            strategy["procedure"] = [
                "Execute functional test.",
                "Observe system behavior.",
                "Document results."
            ]

            strategy["acceptance"] = [
                "Requirement successfully demonstrated."
            ]

            strategy["evidence"] = [
                "Executed protocol"
            ]

        return strategy