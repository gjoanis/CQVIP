class Project:
    """
    Represents a CQV Project.
    A project contains one or more assets.
    """

    def __init__(self, name):
        self.name = name
        self.assets = []

    def add_asset(self, asset):
        self.assets.append(asset)

    def get_assets(self):
        return self.assets

    def display(self):
        print(f"\nProject: {self.name}")

        for asset in self.assets:
            print(f" - {asset.name}")