from datetime import datetime


class DocumentControl:

    def __init__(self, config):

        self.config = config

    def build(self, document_type):

        return {

            "project": self.config.PROJECT_NAME,

            "document_number":
                f"{self.config.PROJECT_CODE}-{document_type}-001",

            "revision":
                "00",

            "status":
                "Draft",

            "prepared_by":
                self.config.AUTHOR,

            "approved_by":
                self.config.APPROVER,

            "date":
                datetime.today().strftime("%Y-%m-%d")

        }