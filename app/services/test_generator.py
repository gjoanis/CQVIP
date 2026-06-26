from app.models.test_case import TestCase


class TestGenerator:
    """
    Generates protocol-style test cases from requirements.
    """

    def __init__(self, requirements):
        self.requirements = requirements
        self.generated_tests = []

    def create_test_step(self, requirement):
        category = requirement.category

        if category == "Alarm":
            return "Challenge the alarm condition and verify the alarm activates as expected."
        elif category == "Cleaning":
            return "Execute the cleaning cycle and verify completion without failure."
        elif category == "Data Integrity":
            return "Verify the system records and retains required data accurately."
        elif category == "Environmental":
            return "Verify the system maintains the required operating condition."
        elif category == "Safety":
            return "Challenge the safety function and verify unsafe operation is prevented."
        elif category == "Operational":
            return "Verify required SOP or training control is in place."
        else:
            return "Verify the system meets the stated requirement."

    def generate_tests(self):
        counter = 1

        for requirement in self.requirements:
            test = TestCase(
                f"TEST-{counter:03}",
                self.create_test_step(requirement),
                requirement.recommended_verification
            )

            self.generated_tests.append(test)
            counter += 1

        return self.generated_tests

    def display_tests(self):
        print("\nGENERATED PROTOCOL TESTS")
        print("-" * 45)

        for test in self.generated_tests:
            test.display()