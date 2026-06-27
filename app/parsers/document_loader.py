from docx import Document as WordDocument


class DocumentLoader:

    @staticmethod
    def load_txt(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def load_docx(filepath):
        document = WordDocument(filepath)

        paragraphs = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n".join(paragraphs)