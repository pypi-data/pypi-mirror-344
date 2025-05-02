import os
import json
import requests
import logging

logger = logging.getLogger(__name__)

# Эндпоинт Gemini Flash (можно сделать настраиваемым через env)
GEMINI_FLASH_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"


def call_gemini_flash(messages_to_summarize: list[dict]) -> str | None:
    """Calls the Gemini API to summarize the provided message history."""
    logger.debug(f"Запрос на суммирование {len(messages_to_summarize)} сообщений.")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY не установлен. Суммирование невозможно.")
        return None

    gemini_flash_url = f"{GEMINI_FLASH_ENDPOINT}?key={api_key}"
    headers = {"Content-Type": "application/json"}

    # Формируем строку истории для промпта
    history_string = "\n".join(
        [
            f"{msg.get('role', 'unknown')}: {msg.get('content', '')}"
            for msg in messages_to_summarize
            if msg.get(
                "content"
            )  # Пропускаем сообщения без контента (например, пустые tool_calls)
        ]
    )

    if not history_string:
        logger.warning("Нет сообщений с контентом для суммирования.")
        return None

    prompt = f"Please concisely summarize the key points, decisions, and outcomes of the following conversation history:\n\n{history_string}"

    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,  # Низкая температура для более фактологичного саммари
            "maxOutputTokens": 1024,  # Ограничение длины саммари
        },
    }
    logger.debug(f"Payload для Gemini (summarize): {json.dumps(payload)[:200]}...")

    try:
        logger.info("Вызов Gemini Flash API для суммирования...")
        response = requests.post(
            gemini_flash_url, headers=headers, json=payload, timeout=120
        )  # Таймаут 120 сек
        response.raise_for_status()  # Вызовет исключение для 4xx/5xx
        response_json = response.json()
        logger.debug(
            f"Ответ Gemini (summarize) JSON: {json.dumps(response_json)[:200]}..."
        )

        candidates = response_json.get("candidates", [])
        if candidates:
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if parts:
                summary = parts[0].get("text")
                if summary:
                    logger.info(
                        f"Суммаризация ({len(summary)} символов) успешно получена."
                    )
                    return summary.strip()

        logger.warning(f"Не удалось извлечь саммари из ответа Gemini: {response_json}")
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка вызова Gemini API (summarize): {e}", exc_info=True)
        if e.response is not None:
            logger.error(f"Текст ответа Gemini (summarize): {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"Неожиданная ошибка при суммировании: {e}", exc_info=True)
        return None
