class Asset:
    """
    Represents a GMP asset (equipment, utility, facility, or system)
    and maintains its lifecycle documentation.
    """

    def __init__(
        self,
        name,
        asset_type,
        facility=None,
        project=None,
        system=None,
    ):

        self.name = name
        self.asset_type = asset_type

        self.facility = facility
        self.project = project
        self.system = system

        self.documents = []

    def add_document(self, document):

        self.documents.append(document)

    def get_documents(self):

        return self.documents

    def get_documents_by_stage(self, lifecycle_stage):

        return [

            document

            for document in self.documents

            if getattr(
                document,
                "lifecycle_stage",
                None,
            ) == lifecycle_stage

        ]

    def get_documents_by_type(self, document_type):

        return [

            document

            for document in self.documents

            if getattr(
                document,
                "document_type",
                None,
            ) == document_type

        ]

    def display(self):

        print("\n" + "=" * 80)

        print(f"Asset     : {self.name}")

        print(f"Type      : {self.asset_type}")

        if self.facility:
            print(f"Facility  : {self.facility}")

        if self.project:
            print(f"Project   : {self.project}")

        if self.system:
            print(f"System    : {self.system}")

        print("=" * 80)

        if not self.documents:

            print("No documents loaded.")

            return

        for document in self.documents:

            print(f"\nDocument          : {document.name}")

            if hasattr(document, "document_type"):
                print(f"Type              : {document.document_type}")

            if hasattr(document, "lifecycle_stage"):
                print(f"Lifecycle Stage   : {document.lifecycle_stage}")

            requirement_count = len(
                getattr(document, "requirements", [])
            )

            print(f"Requirements      : {requirement_count}")