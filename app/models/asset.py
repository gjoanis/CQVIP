class Asset:
    """
    Represents a qualified asset such as equipment,
    a utility, or a facility system.
    """

    def __init__(self, name, asset_type):
        self.name = name
        self.asset_type = asset_type
        self.documents = []

    def add_document(self, document):
        self.documents.append(document)

    def get_documents(self):
        return self.documents

    def display(self):
        print(f"\nAsset: {self.name}")
        print(f"Type : {self.asset_type}")

        for document in self.documents:
            print(f" - {document.title}")