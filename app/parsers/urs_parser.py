import re

from app.models.requirement import Requirement
from app.services.ai_requirement_analyzer import AIRequirementAnalyzer


class URSParser:
    """
    Extracts requirements from URS text.
    Supports auto-numbered requirements and existing IDs like URS-001 or REQ-001.
    """

    def __init__(self, text):
        self.text = text

    def extract_requirement_id(self, line, counter):
        match = re.match(
            r"^(URS[-_ ]?\d+|REQ[-_ ]?\d+|FRS[-_ ]?\d+|DS[-_ ]?\d+)\s*[-:|]*\s*(.*)",
            line,
            re.IGNORECASE
        )

        if match:
            req_id = match.group(1).replace("_", "-").replace(" ", "-").upper()
            req_text = match.group(2).strip()

            if not req_text:
                req_text = line

            return req_id, req_text

        return f"URS-{counter:03}", line

    def assign_demo_status(self, index):
        pattern = [
            "Verified",
            "In Progress",
            "Open",
        ]

        return pattern[index % 3]

    def extract_requirements(self):
        requirements = []
        counter = 1

        lines = self.text.replace("\r", "").split("\n")

        for line in lines:
            line = line.strip()

            if not line:
                continue

            lowered = line.lower()

            is_requirement = (
                "shall" in lowered
                or "must" in lowered
                or re.match(r"^(URS|REQ|FRS|DS)[-_ ]?\d+", line, re.IGNORECASE)
            )

            if not is_requirement:
                continue

            skip_phrases = [
                "this document sets forth",
                "requirement mandated",
                "requirements specified",
                "requirements generation",
                "the following table summarizes",
                "shall be the contractor’s responsibility",
                "shall be the contractor's responsibility",
                "turnover package shall be supplied",
                "requirement specification identification",
            ]

            if any(phrase in lowered for phrase in skip_phrases):
                continue

            req_id, req_text = self.extract_requirement_id(line, counter)

            req_text = re.sub(r"\s+", " ", req_text).strip()
            req_text = re.sub(r"^[BQSO]\s*\|\s*", "", req_text).strip()

            if len(req_text) < 20:
                continue

            ai = AIRequirementAnalyzer()
            analysis = ai.analyze(req_text)

            category = analysis["category"]
            verification = analysis["verification"]
            criticality = analysis["criticality"]

            requirement = Requirement(
                req_id,
                req_text,
                category,
            )

            requirement.risk = analysis.get("risk")
            requirement.gmp_reference = analysis.get("gmp_reference")
            requirement.acceptance_criteria = analysis.get("acceptance_criteria")
            requirement.suggested_test = analysis.get("suggested_test")
            requirement.inspection_concern = analysis.get("inspection_concern")
            requirement.protocol_section = analysis.get("protocol_section")
            requirement.test_steps = analysis.get("test_steps", [])
            requirement.objective_evidence = analysis.get("objective_evidence", [])

            requirement.set_recommended_verification(verification)
            requirement.set_criticality(criticality)

            status = self.assign_demo_status(counter - 1)

            requirement.status = status
            requirement.verified = status == "Verified"

            requirements.append(requirement)

            counter += 1

        return requirements