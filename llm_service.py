
from groq import AsyncGroq
import config

class GroqService:
    """Асинхронный сервис для взаимодействия с Groq API."""
    
    def __init__(self):
        # Инициализируем асинхронный клиент, передавая ключ из конфига
        self.client = AsyncGroq(api_key=config.API_KEY)

    def get_system_instruction(self) -> str:
        """Формирует жесткие правила для исключения галлюцинаций ИИ."""
        return (
            "Вы — строгий ИИ-аналитик юридических документов. Вам предоставлен массив нормативно-правовых актов.\n"
            "Ваша задача: Составить единый, сквозной аналитический саммари-отчет по всей предоставленной информации.\n\n"
            "ПРАВИЛА ЖЕСТКОГО КОНТРОЛЯ ГАЛЛЮЦИНАЦИЙ:\n"
            "1. Опирайтесь ТОЛЬКО на предоставленный текст внутри тегов <document>. Не используйте внешние знания, "
            "не придумывайте законы, не дописывайте последствия норм, которых нет в исходных данных.\n"
            "2. Если информации по какой-то теме нет в тексте, полностью проигнорируйте эту тему.\n"
            "3. Ответ должен быть строго детерминированным, сухим, в профессиональном юридическом стиле.\n\n"
            "ФОРМАТ ВЫВОДА:\n"
            "Сгруппируйте информацию по ключевым правовым институтам и темам, которые содержатся в файлах "
            "(например: 'Осуществление гражданских прав', 'Способы защиты прав', 'Градостроительная деятельность').\n"
            "Указывайте точное имя файла в квадратных скобках [Источник: имя_файла] для каждого ключевого тезиса.\n"
            "Вывод должен быть строго на русском языке в формате Markdown с понятной и четкой структурой."
        )

    async def generate_summary(self, documents_payload: str) -> str:
        """Отправляет упакованный контекст документов в Groq API."""
        messages = [
            {"role": "system", "content": self.get_system_instruction()},
            {"role": "user", "content": f"Вот документы для анализа:\n\n{documents_payload}\n\nПроанализируй их и составь итоговый отчет."}
        ]
    
        response = await self.client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=messages,
            temperature=config.TEMPERATURE,
            max_completion_tokens=16384,
            reasoning_effort="none"
        )
        return response.choices[0].message.content






    # async def generate_summary(self, documents_payload: str) -> str:
    #     """Отправляет упакованный контекст документов в Groq API."""
    #     # Для моделей Llama инструкции системы и пользователя передаются в виде списка сообщений (messages)
    #     messages = [
    #         {
    #             "role": "system",
    #             "content": self.get_system_instruction()
    #         },
    #         {
    #             "role": "user",
    #             "content": f"Вот документы для анализа:\n\n{documents_payload}\n\nПроанализируй их и составь итоговый отчет."
    #         }
    #     ]
        
    #     # Делаем асинхронный запрос к модели
    #     response = await self.client.chat.completions.create(
    #         model=config.MODEL_NAME,
    #         messages=messages,
    #         temperature=config.TEMPERATURE
    #     )
        
    #     # Возвращаем сгенерированный текст отчета
    #     return response.choices[0].message.content
