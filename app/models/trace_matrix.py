class TraceMatrix:
    """
    Stores end-to-end traceability between requirements and verification.
    """

    def __init__(self):
        self.matrix = {}

    def add_link(self, requirement_id, test_id):
        if requirement_id not in self.matrix:
            self.matrix[requirement_id] = []

        self.matrix[requirement_id].append(test_id)

    def get_tests(self, requirement_id):
        return self.matrix.get(requirement_id, [])

    def display(self):
        print("\n=== TRACEABILITY MATRIX ===")

        for requirement, tests in self.matrix.items():
            print(f"{requirement} -> {tests}")