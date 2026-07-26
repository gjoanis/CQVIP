class Document:
    """
    Represents a single document within the CQV lifecycle.
    """

    def __init__(
        self,
        system_id,
        lifecycle_stage_id,
        document_type_id,
        filename,
        file_path,
        title=None,
        original_filename=None,
        revision=None,
        document_number=None,
        description=None,
        status="Draft",
        effective_date=None,
        uploaded_by=None,
        uploaded_date=None,
        supersedes_document_id=None,
        document_id=None,
    ):

        self.id = document_id

        self.system_id = system_id

        self.lifecycle_stage_id = lifecycle_stage_id
        self.document_type_id = document_type_id

        self.lifecycle_stage = None
        self.document_type = None

        self.title = title
        self.filename = filename
        self.original_filename = original_filename
        self.file_path = file_path

        self.name = title or filename

        self.revision = revision
        self.document_number = document_number
        self.description = description

        self.status = status

        self.effective_date = effective_date

        self.uploaded_by = uploaded_by
        self.uploaded_date = uploaded_date

        self.supersedes_document_id = supersedes_document_id

        self.is_current = True

        self.ai_processed = False
        self.ai_summary = None

        self.requirements = []

    def add_requirement(self, requirement):

        requirement.document_id = self.id

        if hasattr(requirement, "document_name"):
            requirement.document_name = self.name

        if hasattr(requirement, "document_type"):
            requirement.document_type = self.document_type

        if hasattr(requirement, "lifecycle_stage"):
            requirement.lifecycle_stage = self.lifecycle_stage

        self.requirements.append(requirement)

    def requirement_count(self):

        return len(self.requirements)

    def get_requirements(self):

        return self.requirements

    def __repr__(self):

        return (
            f"<Document("
            f"{self.name}, "
            f"{self.document_type}, "
            f"{self.lifecycle_stage})>"
        )