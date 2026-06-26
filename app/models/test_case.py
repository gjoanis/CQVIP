class TestCase:
    """
    Represents an IQ, OQ, PQ, FAT, SAT, or Commissioning test.
    """

    def __init__(self, test_id, name, phase):
        self.test_id = test_id
        self.name = name
        self.phase = phase
        self.requirements = []
        self.status = "Not Executed"

    def link_requirement(self, requirement):
        self.requirements.append(requirement)

    def execute(self):
        self.status = "Passed"

    def fail(self):
        self.status = "Failed"

    def display(self):
        print(f"\nTest ID : {self.test_id}")
        print(f"Name    : {self.name}")
        print(f"Phase   : {self.phase}")
        print(f"Status  : {self.status}")