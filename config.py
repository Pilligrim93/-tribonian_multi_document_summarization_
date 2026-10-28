
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Считываем ключ Groq
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("Критическая ошибка: GROQ_API_KEY не найден в файле .env")

# Абсолютные пути к директориям проекта
BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "documents"
OUTPUT_DIR = BASE_DIR / "output"

# Настройки ИИ-модели от Groq
MODEL_NAME = "qwen/qwen3.8-27b"  # Мощная, точная и бесплатная модель на Groq
TEMPERATURE = 0.0                     # Strict mode (строгий режим без фантазий)
