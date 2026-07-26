import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from app.parsers.document_loader import DocumentLoader

load_dotenv()


class DocumentAIService:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def extract_text(self, file_path: str) -> str:

        return DocumentLoader.load(file_path)

    def analyze_requirement(

        self,

        requirement_text: str,

        document_text: str,

        document_type: str = "",

        lifecycle_stage: str = "",

    ):

        prompt = f"""
You are a senior GMP validation consultant.

Lifecycle Stage:
{lifecycle_stage}

Document Type:
{document_type}

Requirement:
{requirement_text}

Supporting Document:
{document_text[:12000]}

Evaluate whether the uploaded lifecycle document satisfies the requirement.

Return JSON only.

{{
    "summary":"",
    "match":"Full|Partial|None",
    "gap_analysis":"",
    "recommendation":"",
    "objective_evidence":[],
    "inspection_risk":"Low|Medium|High"
}}
"""

        response = self.client.chat.completions.create(

            model="gpt-4.1",

            response_format={
                "type": "json_object"
            },

            messages=[

                {

                    "role": "system",

                    "content": (
                        "You are an expert in FDA, EMA, Annex 11, Annex 15, "
                        "GAMP 5, CQV, CSV, Data Integrity and GMP validation."
                    ),

                },

                {

                    "role": "user",

                    "content": prompt,

                },

            ],

        )

        return json.loads(

            response.choices[0].message.content

        )

    def analyze_document(

        self,

        requirement_text: str,

        file_path: str,

        document_type: str = "",

        lifecycle_stage: str = "",

    ):

        text = self.extract_text(file_path)

        if not text.strip():

            return {

                "summary": "",

                "match": "None",

                "gap_analysis": "Unable to extract document text.",

                "recommendation": "Verify the uploaded document.",

                "objective_evidence": [],

                "inspection_risk": "High",

            }

        return self.analyze_requirement(

            requirement_text=requirement_text,

            document_text=text,

            document_type=document_type,

            lifecycle_stage=lifecycle_stage,

        )