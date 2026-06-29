class AIRequirementAnalyzer:

    def analyze(self, requirement_text):
        text = requirement_text.lower()

        if "hepa" in text or "particle" in text or "air changes" in text:
            return {
                "category": "Environmental",
                "criticality": "Critical",
                "verification": "OQ",
                "risk": "High",
                "suggested_test": "Verify cleanroom environmental conditions against specified classification limits.",
                "inspection_concern": "Evidence must show environmental control under qualified operating conditions."
            }

        if "fire" in text or "safety" in text:
            return {
                "category": "Safety",
                "criticality": "Critical",
                "verification": "OQ",
                "risk": "High",
                "suggested_test": "Verify safety systems are installed and functional.",
                "inspection_concern": "Safety-related requirements require documented objective evidence."
            }

        if "occupant limit" in text:
            return {
                "category": "Operational",
                "criticality": "Major",
                "verification": "SOP / Training",
                "risk": "Medium",
                "suggested_test": "Verify room occupancy limits are defined, posted, and controlled by procedure.",
                "inspection_concern": "Occupancy control should be supported by procedure and training evidence."
            }

        return {
            "category": "Functional",
            "criticality": "Minor",
            "verification": "Commissioning / IQ / OQ",
            "risk": "Low",
            "suggested_test": "Verify requirement through commissioning or qualification evidence.",
            "inspection_concern": "Requirement should be traceable to objective evidence."
        }