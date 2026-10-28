
import asyncio
import logging
import config
from parser import DocumentParser
from llm_service import GroqService

# Настраиваем логирование, чтобы видеть прогресс в консоли
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def main():
    logging.info("Запуск системы суммаризации юридических документов на базе Groq...")
    
    # 1. Инициализируем парсер и ИИ-сервис
    parser = DocumentParser(config.DOCS_DIR)
    ai_service = GroqService()
    
    # 2. Сканируем и считываем документы из папки documents
    raw_docs = parser.load_all_documents()
    if not raw_docs:
        logging.warning(f"Папка {config.DOCS_DIR} пуста. Положи туда PDF или TXT файлы из ТЗ.")
        return

    logging.info(f"Успешно считано документов: {len(raw_docs)}. Упаковка контекста...")
    
    # 3. Формируем единую XML-структуру для отправки в ИИ
    payload = parser.build_xml_payload(raw_docs)
    
    # 4. Отправляем данные в Groq
    logging.info("Отправка запроса в Groq API (ожидайте генерации отчета)...")
    try:
        summary_result = await ai_service.generate_summary(payload)
        
        # 5. Сохраняем готовый отчет в папку output
        output_file = config.OUTPUT_DIR / "summary_report.md"
        output_file.write_text(summary_result, encoding="utf-8")
        
        logging.info(f"Анализ успешно завершен! Отчет сохранен в: {output_file}")
        
    except Exception as e:
        logging.critical(f"Произошла ошибка во время выполнения запроса: {e}")

if __name__ == "__main__":
    # Запуск асинхронного пайплайна через asyncio
    asyncio.run(main())
