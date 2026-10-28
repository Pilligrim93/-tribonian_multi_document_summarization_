
import pdfplumber
from pathlib import Path
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DocumentParser:
    """Класс для безопасного извлечения текста из локальных документов."""
    
    def __init__(self, docs_dir: Path):
        self.docs_dir = docs_dir

    def extract_text_from_pdf(self, file_path: Path) -> str:
        """Извлекает текст из PDF-файла постранично."""
        text_content = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
            return "\n".join(text_content)
        except Exception as e:
            logging.error(f"Ошибка при чтении PDF {file_path.name}: {e}")
            return ""

    def extract_text_from_txt(self, file_path: Path) -> str:
        """Читает обычный текстовый файл."""
        try:
            return file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                return file_path.read_text(encoding="windows-1251")
            except Exception as e:
                logging.error(f"Не удалось прочитать TXT {file_path.name}: {e}")
                return ""

    def load_all_documents(self) -> List[Dict[str, str]]:
        """Сканирует папку и собирает данные документов."""
        loaded_docs = []
        extensions = ["*.pdf", "*.txt"]
        
        for ext in extensions:
            for file_path in self.docs_dir.glob(ext):
                logging.info(f"Парсинг файла: {file_path.name}")
                
                if file_path.suffix.lower() == ".pdf":
                    content = self.extract_text_from_pdf(file_path)
                else:
                    content = self.extract_text_from_txt(file_path)
                
                if content.strip():
                    loaded_docs.append({
                        "filename": file_path.name,
                        "content": content.strip()
                    })
        
        return loaded_docs

    @staticmethod
    def build_xml_payload(documents: List[Dict[str, str]]) -> str:
        """Упаковывает тексты в XML-структуру для предотвращения смешивания контекстов."""
        payload = []
        for doc in documents:
            payload.append(f'<document name="{doc["filename"]}">\n{doc["content"]}\n</document>')
        return "\n\n".join(payload)
