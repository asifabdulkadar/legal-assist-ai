import os
import pdfplumber
import docx
from typing import List, Dict, Any

class DocumentParser:
    """Handles text extraction from various document formats (PDF, DOCX, TXT)."""
    
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """Extracts text from a PDF file using pdfplumber for better structure retention."""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error parsing PDF {file_path}: {e}")
        return text

    @staticmethod
    def parse_docx(file_path: str) -> str:
        """Extracts text from a DOCX file."""
        text = ""
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error parsing DOCX {file_path}: {e}")
        return text

    @staticmethod
    def parse_txt(file_path: str) -> str:
        """Extracts text from a plain text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            print(f"Error parsing TXT {file_path}: {e}")
            return ""

    def parse(self, file_path: str) -> str:
        """Main method to parse a document based on its extension."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return self.parse_pdf(file_path)
        elif ext in ['.doc', '.docx']:
            return self.parse_docx(file_path)
        elif ext == '.txt':
            return self.parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @staticmethod
    def clean_text(text: str) -> str:
        """Basic text cleaning."""
        # Replace multiple newlines with a single newline (or double for paragraph separation)
        import re
        text = re.sub(r'\n\s*\n', '\n\n', text)
        # Remove excessive whitespace
        text = re.sub(r' +', ' ', text)
        return text.strip()
