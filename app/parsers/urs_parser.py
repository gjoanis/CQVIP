import re

from app.models.requirement import Requirement
from app.services.ai_requirement_analyzer import AIRequirementAnalyzer


class URSParser:
    """
    Extracts requirements from lifecycle documents and enriches them
    with AI metadata.
    """

    def __init__(self, text):

        self.text = text
        self.ai = AIRequirementAnalyzer()

    def extract_requirement_id(self, line, counter):

        match = re.match(
            r"^(URS[-_ ]?\d+|REQ[-_ ]?\d+|FRS[-_ ]?\d+|DS[-_ ]?\d+|IQ[-_ ]?\d+|OQ[-_ ]?\d+|PQ[-_ ]?\d+|DQ[-_ ]?\d+|FAT[-_ ]?\d+|SAT[-_ ]?\d+)\s*[-:|]*\s*(.*)",
            line,
            re.IGNORECASE,
        )

        if match:

            req_id = (
                match.group(1)
                .replace("_", "-")
                .replace(" ", "-")
                .upper()
            )

            req_text = match.group(2).strip()

            if not req_text:
                req_text = line

            return req_id, req_text

        return f"REQ-{counter:04}", line

    def assign_demo_status(self, index):

        pattern = [
            "Verified",
            "In Progress",
            "Open",
        ]

        return pattern[index % len(pattern)]

    def enrich_requirement(self, requirement):

        try:

            analysis = self.ai.analyze(
                requirement.text
            )

            requirement.category = analysis.get(
                "category",
                "General",
            )

            requirement.risk = analysis.get(
                "risk",
                "Medium",
            )

            requirement.gmp_reference = analysis.get(
                "gmp_reference",
                "Not Available",
            )

            requirement.acceptance_criteria = analysis.get(
                "acceptance_criteria",
                "Not Available",
            )

            requirement.suggested_test = analysis.get(
                "suggested_test",
                "Functional Verification",
            )

            requirement.inspection_concern = analysis.get(
                "inspection_concern",
                "",
            )

            requirement.protocol_section = analysis.get(
                "protocol_section",
                "Not Assigned",
            )

            requirement.regulatory_rationale = analysis.get(
                "regulatory_rationale",
                "",
            )

            requirement.regulatory_sources = analysis.get(
                "regulatory_sources",
                [],
            )

            requirement.test_steps = analysis.get(
                "test_steps",
                [],
            )

            requirement.objective_evidence = analysis.get(
                "objective_evidence",
                [],
            )

            requirement.set_recommended_verification(

                analysis.get(
                    "verification_strategy",
                    "Test",
                )

            )

            requirement.set_criticality(

                analysis.get(
                    "criticality",
                    "Medium",
                )

            )

        except Exception:

            requirement.category = "General"
            requirement.risk = "Medium"
            requirement.gmp_reference = "Not Available"
            requirement.acceptance_criteria = "Not Available"
            requirement.suggested_test = "Functional Verification"
            requirement.inspection_concern = ""
            requirement.protocol_section = "Not Assigned"
            requirement.regulatory_rationale = ""
            requirement.regulatory_sources = []
            requirement.test_steps = []
            requirement.objective_evidence = []

            requirement.set_recommended_verification(
                "Test"
            )

            requirement.set_criticality(
                "Medium"
            )

    def extract_requirements(self):

        requirements = []

        counter = 1

        lines = self.text.replace(
            "\r",
            "",
        ).split("\n")

        for line in lines:

            line = line.strip()

            if not line:
                continue

            lowered = line.lower()

            is_requirement = (

                " shall " in f" {lowered} "

                or " must " in f" {lowered} "

                or re.match(
                    r"^(URS|REQ|FRS|DS|DQ|FAT|SAT|IQ|OQ|PQ)[-_ ]?\d+",
                    line,
                    re.IGNORECASE,
                )

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

            if any(
                phrase in lowered
                for phrase in skip_phrases
            ):
                continue

            req_id, req_text = self.extract_requirement_id(
                line,
                counter,
            )

            req_text = re.sub(
                r"\s+",
                " ",
                req_text,
            ).strip()

            req_text = re.sub(
                r"^[BQSO]\s*\|\s*",
                "",
                req_text,
            ).strip()

            if len(req_text) < 20:
                continue

            requirement = Requirement(

                req_id=req_id,

                source_req_id=req_id,

                system_id=None,

                document_id=None,

                text=req_text,

                category="General",

            )

            self.enrich_requirement(
                requirement
            )

            status = self.assign_demo_status(
                counter - 1
            )

            requirement.status = status
            requirement.verified = (
                status == "Verified"
            )

            requirements.append(
                requirement
            )

            counter += 1

        return requirements