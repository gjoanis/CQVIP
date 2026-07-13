class DashboardReport:
    """
    Displays project and validation dashboard information.
    """

    def __init__(self, project, asset):
        self.project = project
        self.asset = asset

    def display(self):

        requirements = []

        for document in self.asset.documents:
            requirements.extend(document.requirements)

        total = len(requirements)

        verified = sum(
            1 for requirement in requirements
            if requirement.verified
        )

        coverage = (
            (verified / total) * 100
            if total else 0
        )

        lifecycle = {
            "DQ": 0,
            "FAT": 0,
            "SAT": 0,
            "Commissioning": 0,
            "IQ": 0,
            "OQ": 0,
            "PQ": 0,
        }

        high = medium = low = 0

        for requirement in requirements:

            if requirement.criticality == "High":
                high += 1
            elif requirement.criticality == "Medium":
                medium += 1
            elif requirement.criticality == "Low":
                low += 1

            for phase in lifecycle:
                if requirement.lifecycle_tests.get(phase):
                    lifecycle[phase] += 1

        print("\nCQVIP VALIDATION DASHBOARD")
        print("=" * 50)

        print("Project :", self.project.name)
        print("Asset   :", self.asset.name)
        print("Type    :", self.asset.asset_type)
        print("Documents:", len(self.asset.documents))

        print("\nPROJECT METRICS")
        print("-" * 50)
        print(f"Requirements        : {total}")
        print(f"Verified            : {verified}")
        print(f"Coverage            : {coverage:.1f}%")

        print("\nLIFECYCLE COVERAGE")
        print("-" * 50)

        for phase, count in lifecycle.items():
            percent = (count / total * 100) if total else 0
            print(f"{phase:<15}{count:>3}/{total:<3} ({percent:.0f}%)")

        print("\nRISK DISTRIBUTION")
        print("-" * 50)
        print(f"High   : {high}")
        print(f"Medium : {medium}")
        print(f"Low    : {low}")

        readiness = (
            "Inspection Ready"
            if coverage >= 90
            else "In Progress"
        )

        print("\nINSPECTION READINESS")
        print("-" * 50)
        print(f"Status : {readiness}")