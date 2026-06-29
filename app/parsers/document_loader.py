from docx import Document as WordDocument


class DocumentLoader:

    @staticmethod
    def load_txt(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def load_docx(filepath):
        document = WordDocument(filepath)

        text_blocks = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()
            if text:
                text_blocks.append(text)

        for table in document.tables:
            for row in table.rows:
                cells = []

                for cell in row.cells:
                    cell_text = cell.text.strip()

                    if cell_text:
                        cells.append(cell_text)

                if cells:
                    text_blocks.append(" | ".join(cells))

        return "\n".join(text_blocks)