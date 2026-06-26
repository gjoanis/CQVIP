class Document:
    """
    Represents a CQV document such as a URS, SIA, FAT, SAT, IQ, OQ, or PQ.
    """

    def __init__(self, title, document_type):
        self.title = title
        self.document_type = document_type
        self.requirements = []

    def add_requirement(self, requirement):
        self.requirements.append(requirement)

    def get_requirements(self):
        return self.requirements

    def display(self):
        print(f"\nDocument: {self.title}")
        print(f"Type    : {self.document_type}")

        for requirement in self.requirements:
            print(f" - {requirement.req_id}: {requirement.text}")