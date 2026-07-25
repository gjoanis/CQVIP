import json
import os
from pathlib import Path

import pypdf
from docx import Document
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class DocumentAIService:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def extract_text(self, file_path: str) -> str:

        suffix = Path(file_path).suffix.lower()

        if suffix == ".pdf":
            return self._extract_pdf(file_path)

        if suffix == ".docx":
            return self._extract_docx(file_path)

        if suffix == ".txt":
            return Path(file_path).read_text(
                encoding="utf-8",
                errors="ignore",
            )

        return ""

    def analyze_requirement(
        self,
        requirement_text: str,
        document_text: str,
    ):

        prompt = f"""
You are an FDA GMP validation expert.

Requirement:

{requirement_text}

Supporting Document:

{document_text[:12000]}

Evaluate the document against the requirement.

Return JSON with exactly these fields:

{{
    "summary":"",
    "match":"Full | Partial | None",
    "gap_analysis":"",
    "recommendation":""
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
                        "You are a senior GMP validation "
                        "consultant specializing in CQV."
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
    ):

        text = self.extract_text(file_path)

        if not text.strip():

            return {
                "summary": "",
                "match": "None",
                "gap_analysis": "Unable to extract document text.",
                "recommendation": (
                    "Verify the uploaded document."
                ),
            }

        return self.analyze_requirement(
            requirement_text,
            text,
        )

    def _extract_pdf(
        self,
        file_path: str,
    ):

        text = ""

        reader = pypdf.PdfReader(file_path)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    def _extract_docx(
        self,
        file_path: str,
    ):

        document = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )