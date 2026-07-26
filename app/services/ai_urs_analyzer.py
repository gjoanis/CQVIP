import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class AIURSAnalyzer:

    def analyze(self, requirement):

        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        prompt = f"""
You are a senior GMP Commissioning, Qualification and Validation engineer.

Analyze the following User Requirement Specification (URS).

Requirement:

{json.dumps(requirement, indent=2)}

Return ONLY valid JSON in exactly this format:

{{
  "req_id": "{requirement["req_id"]}",
  "category": "",
  "criticality": "",
  "verification": "",
  "risk": "",
  "gmp_reference": "",
  "acceptance_criteria": "",
  "suggested_test": "",
  "inspection_concern": "",
  "protocol_section": "",
  "test_steps": [],
  "objective_evidence": []
}}

Do not wrap the JSON in markdown.
Do not include explanations.
Return ONLY the JSON object.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert GMP validation engineer. Always return valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content.strip()

        return json.loads(content)