class ValidationPackage:

    def __init__(self):
        self.documents = []

    def add(self, document):
        self.documents.append(document)

    def build(self):

        print("\nBUILDING VALIDATION PACKAGE")
        print("-" * 40)

        for document in self.documents:
            document.generate()

        print("\nValidation Package Complete.")