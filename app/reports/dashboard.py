class DashboardReport:
    """
    Displays project and asset dashboard information.
    """

    def __init__(self, project, asset):
        self.project = project
        self.asset = asset

    def display(self):
        print("\nCQVIP DASHBOARD")
        print("=" * 45)
        print("Project:", self.project.name)
        print("Asset:", self.asset.name)
        print("Asset Type:", self.asset.asset_type)
        print("Documents:", len(self.asset.documents))