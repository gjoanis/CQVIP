from app.models.test_case import TestCase
from app.services.verification_strategy import VerificationStrategy


class TestGenerator:
    """
    Generates lifecycle verification test cases from analyzed requirements.
    """

    def __init__(self, requirements):
        self.requirements = requirements
        self.generated_tests = []
        self.strategy_builder = VerificationStrategy()

    def phase_label(self, phase_key):
        labels = {
            "dq": "DQ",
            "fat": "FAT",
            "sat": "SAT",
            "commissioning": "Commissioning",
            "iq": "IQ",
            "oq": "OQ",
            "pq": "PQ",
        }

        return labels.get(phase_key, "Qualification")

    def determine_name(self, requirement, phase):
        category = requirement.category or "Requirement"
        return f"{phase} - Verify {category}"

    def generate_tests(self):
        self.generated_tests = []
        counter = 1

        for requirement in self.requirements:
            strategy = self.strategy_builder.build(requirement)

            for phase_key, activities in strategy.items():
                phase = self.phase_label(phase_key)

                for activity in activities:
                    test_id = f"TEST-{counter:03}"

                    test = TestCase(
                        test_id,
                        self.determine_name(requirement, phase),
                        phase
                    )

                    requirement.add_lifecycle_test(phase, test_id)

                    test.requirement_id = requirement.req_id
                    test.requirement_text = requirement.text
                    test.test_step = activity
                    test.acceptance_criteria = requirement.acceptance_criteria
                    test.objective_evidence = requirement.objective_evidence
                    test.regulatory_sources = requirement.regulatory_sources
                    test.regulatory_rationale = requirement.regulatory_rationale

                    self.generated_tests.append(test)
                    counter += 1

        return self.generated_tests

    def display_tests(self):
        print("\nGENERATED PROTOCOL TESTS")
        print("-" * 60)

        for test in self.generated_tests:
            test.display()

            print("Requirement :", test.requirement_id)
            print("Step        :", test.test_step)

            if test.acceptance_criteria:
                print("Acceptance  :", test.acceptance_criteria)

            if test.objective_evidence:
                print("Evidence:")
                for evidence in test.objective_evidence:
                    print("   •", evidence)

            if test.regulatory_sources:
                print("Sources:")
                for source in test.regulatory_sources:
                    print("   •", source)

            if test.regulatory_rationale:
                print("Rationale:")
                print("   ", test.regulatory_rationale)

            print("-" * 60)