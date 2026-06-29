import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class AIURSAnalyzer:

    def analyze(self, requirements):

        api_key = os.getenv("OPENAI_API_KEY")

        client = OpenAI(api_key=api_key)

        prompt = f"""
You are a senior GMP Commissioning, Qualification and Validation engineer.

Analyze every requirement.

Return ONLY valid JSON.

Requirements:

{json.dumps(requirements, indent=2)}

For EACH requirement return:

[
  {{
    "req_id":"",
    "category":"",
    "criticality":"",
    "verification":"",
    "risk":"",
    "gmp_reference":"",
    "acceptance_criteria":"",
    "suggested_test":"",
    "inspection_concern":"",
    "protocol_section":"",
    "test_steps":[],
    "objective_evidence":[]
  }}
]
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        content = response.choices[0].message.content

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        return json.loads(content)