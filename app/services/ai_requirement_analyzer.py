import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class AIRequirementAnalyzer:

    def analyze_with_openai(self, requirement_text):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            return None

        client = OpenAI(api_key=api_key)

        prompt = f"""
        You are a senior GMP Commissioning, Qualification and Validation engineer with expertise in FDA, EU GMP Annex 1, ISPE Baseline Guides, ASTM E2500, and GAMP5.

        Analyze this URS requirement.

        Requirement:
        {requirement_text}

        Return ONLY valid JSON.

        {{
          "category":"",
          "criticality":"",
          "verification":"",
          "risk":"",
          "suggested_test":"",
          "inspection_concern":"",
          "gmp_reference":"",
          "acceptance_criteria":"",
          "protocol_section":"",
          "test_steps":[
              "",
              "",
              ""
          ],
          "objective_evidence":[
              "",
              ""
          ]
        }}
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )

        content = response.choices[0].message.content.strip()

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        return json.loads(content)

    def analyze(self, requirement_text):
        text = requirement_text.lower()

        # Try OpenAI first
        ai_result = self.analyze_with_openai(requirement_text)

        if ai_result:
            return ai_result

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