#!/usr/bin/env python3
"""
demo_chat_completions.py – пример вызова Chat Completions API c o3 и кастомным тулом 'ask'.
Принимает запрос пользователя как аргумент командной строки.
Использует стандартный цикл Chat Completions API с ручным ведением истории.
"""

import os
import json
import subprocess
import sys
import copy
from openai import OpenAI
from pathlib import Path
import logging
import shlex
import click
import logging.handlers  # Added for FileHandler
from typing import Optional, List, Tuple

# Import config first to load .env before other imports might need env vars
from .core import config

from . import __version__
from .input_utils import get_multiline, prompt_toolkit_available
from .ui_utils import wrap_print, rich_available

# --- Импорт версии (уже импортировано выше) ---
# try:
#     from . import __version__
# except ImportError: # Если запускается не как пакет
#     __version__ = "unknown"

# --- Конфигурация Путей и Логирования ---
# Конфигурация логирования теперь может использовать LOG_LEVEL из config
# Используем Path.cwd() для путей относительно директории запуска
CWD = Path.cwd()
DATA_DIR = CWD / "data" / "thread_history"
LOGS_DIR = CWD / "logs"
HISTORY_FILE = DATA_DIR / "messages.json"

# Создаем директории при старте
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Файл лога
cli_log_file = LOGS_DIR / "assistant_cli.log"

# Настройка логгера для этого модуля ДО настройки хендлеров
logger = logging.getLogger(__name__)  # Get root logger or specific one


def setup_logging(verbose: bool = False):
    """Configures logging with file and console handlers."""
    log_level_console = logging.INFO if verbose else logging.WARNING
    log_level_file = logging.DEBUG  # Always DEBUG for file

    log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # Получаем корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level_file)  # Set root logger level to lowest (DEBUG)

    # Удаляем все существующие хендлеры (например, стандартный basicConfig)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()  # Закрываем хендлер перед удалением

    # --- File Handler ---
    file_handler = logging.FileHandler(cli_log_file, mode="a", encoding="utf-8")
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level_file)
    root_logger.addHandler(file_handler)

    # --- Console Handler ---
    # Используем RichHandler если доступен, иначе StreamHandler
    try:
        # Check if rich is available and not explicitly disabled
        if rich_available:
            from rich.logging import RichHandler

            console_handler = RichHandler(
                rich_tracebacks=True,
                show_time=False,  # Keep console less noisy
                show_level=True,
                show_path=False,
                log_time_format="[%X]",  # Example time format
            )
        else:
            raise ImportError(
                "Rich not available or disabled"
            )  # Fallback to StreamHandler
    except ImportError:
        console_handler = logging.StreamHandler(
            sys.stderr
        )  # Log warnings/errors to stderr
        console_handler.setFormatter(log_formatter)  # Use standard format for fallback

    console_handler.setLevel(log_level_console)
    root_logger.addHandler(console_handler)

    logger.info(
        f"Logging setup complete. Console level: {logging.getLevelName(log_level_console)}, File level: {logging.getLevelName(log_level_file)}"
    )
    logger.debug(f"Verbose mode: {verbose}")


# --- Удаление старой загрузки переменных окружения ---
# Загрузка переменных теперь происходит в config.py
# def load_env_variable(var_name: str, env_file_path: Path) -> str | None:
#     ...
# ENV_FILE_PATH = ...
# OPENAI_API_KEY = ...
# GEMINI_API_KEY = ...
# PERPLEXITY_API_KEY = ...

# --- Проверка наличия ключей API (перемещена в main) ---
# --- Конец проверки ключей API ---

# --- Инициализация клиента OpenAI ---
# Инициализация клиента ТЕПЕРЬ ДОЛЖНА БЫТЬ ВНУТРИ main(), ПОСЛЕ проверки ключей
# try:
#     client = OpenAI(api_key=config.OPENAI_API_KEY)
#     logger.info("Клиент OpenAI успешно инициализирован.")
# except Exception as e:
#     logger.critical(f"Критическая ошибка инициализации клиента OpenAI: {e}", exc_info=True)
#     print(f"\n💥 Error initializing OpenAI client: {e}", file=sys.stderr)
#     print("Please ensure the SDK version is compatible and OPENAI_API_KEY is set.", file=sys.stderr)
#     sys.exit(1)
# --- Конец Инициализации клиента OpenAI ---

# --- НАСТРОЙКА ИНСТРУМЕНТОВ ---

# ❷ Схема для инструмента 'ask' (формат Chat Completions)
#    Обратите внимание: type="function" остается, но name убирается с верхнего уровня
ASK_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "ask",
        "description": "Consults the Lead Software Engineer (ask.py) about the current project. Use this for questions about code implementation, project structure, or high-level advice. The tool has access to the project files and directory tree.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The user's request or question for the Lead Software Engineer.",
                },
            },
            "required": ["query"],
        },
    },
}

# Схема для execute_terminal_command
TERMINAL_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "execute_terminal_command",
        "description": "Executes a shell command in the project workspace and returns the output. Use carefully for tasks like listing files (`ls -l`), checking configurations (`cat some_config.json`), running linters, or simple scripts. Specify the command and optionally stdin or a working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute.",
                },
                "stdin": {
                    "type": ["string", "null"],
                    "description": "Optional standard input to pass to the command.",
                },
                "cwd": {
                    "type": ["string", "null"],
                    "description": "Optional working directory to run the command in (relative to project root).",
                },
            },
            "required": ["command"],
        },
    },
}

# Схема для create_file
CREATE_FILE_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "create_file",
        "description": "Creates a new file or overwrites an existing file with the specified content. Provide the target file path (relative to project root) and the full content.",
        "parameters": {
            "type": "object",
            "properties": {
                "target_file": {
                    "type": "string",
                    "description": "The path of the file to create or overwrite (relative to project root).",
                },
                "content": {
                    "type": "string",
                    "description": "The full content to write into the file.",
                },
            },
            "required": ["target_file", "content"],
        },
    },
}

# Схема для apply_diff (использует file_modifier.py)
APPLY_DIFF_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "apply_diff",
        "description": "Modifies an existing file based on a requested change or a provided patch/diff. Provide the target file path and either a description of the change or the patch content.",
        "parameters": {
            "type": "object",
            "properties": {
                "target_file": {
                    "type": "string",
                    "description": "The path of the file to modify (relative to project root).",
                },
                "diff_content": {
                    "type": "string",
                    "description": "A description of the desired change OR the patch content (e.g., unified diff format) to apply.",
                },
            },
            "required": ["target_file", "diff_content"],
        },
    },
}

# Схема для Perplexity
PERPLEXITY_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "query_perplexity",
        "description": "Queries the Perplexity AI API (sonar-reasoning-pro model) with a given query and optional file attachments for context. Useful for research, finding code examples, best practices, or external information related to the attached files.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to send to Perplexity AI.",
                },
                "attachments": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of file paths (relative to project root) to attach as context to the query.",
                },
            },
            "required": ["query"],
        },
    },
}

# ❸ Описываем инструменты
# Включаем все доступные схемы инструментов
TOOLS = [
    ASK_TOOL_SCHEMA,
    TERMINAL_TOOL_SCHEMA,
    CREATE_FILE_TOOL_SCHEMA,
    APPLY_DIFF_TOOL_SCHEMA,
    PERPLEXITY_TOOL_SCHEMA,
]
TOOL_CHOICE = "auto"  # Модель сама выбирает инструмент

# --- Импорты бэкенд-функций инструментов ---
try:
    from assistant.tools import (
        execute_terminal_command,
        handle_create_file,
        handle_apply_diff,
        query_perplexity,  # Импортируем query_perplexity
    )

    logger.info("Бэкенды инструментов успешно импортированы.")
except ImportError as e:
    logger.critical(
        f"Критическая ошибка: Не удалось импортировать бэкенды инструментов: {e}",
        exc_info=True,
    )
    print(f"Error: Could not import tool backends: {e}", file=sys.stderr)

    # Определяем заглушки...
    def execute_terminal_command(*args, **kwargs):
        return {"status": "error", "error_message": "Tool backend unavailable"}

    def handle_create_file(*args, **kwargs):
        return False, "Tool backend unavailable"

    def handle_apply_diff(*args, **kwargs):
        return False, "Tool backend unavailable", None

    def query_perplexity(*args, **kwargs):
        return {
            "error": {"message": "Tool backend unavailable"}
        }  # Заглушка для query_perplexity

# --- КОНЕЦ НАСТРОЙКИ ИНСТРУМЕНТОВ ---


# --- Функции для Работы с Историей ---
def load_history() -> list:
    """Загружает ПОЛНУЮ историю сообщений из JSON файла."""
    if not HISTORY_FILE.exists():
        logger.info(f"Файл истории {HISTORY_FILE} не найден, начинаем новую.")
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            if not content:
                logger.info(f"Файл истории {HISTORY_FILE} пуст, начинаем новую.")
                return []
            history = json.loads(content)
            logger.info(
                f"История загружена из {HISTORY_FILE} ({len(history)} сообщений)."
            )
            # TODO: Добавить проверку формата истории?
            if isinstance(history, list):
                return history
            else:
                logger.warning(
                    f"Файл истории {HISTORY_FILE} содержит не список, а {type(history)}. Начинаем новую историю."
                )
                return []
    except json.JSONDecodeError:
        logger.warning(
            f"Файл истории {HISTORY_FILE} поврежден (JSONDecodeError). Начинаем новую историю.",
            exc_info=True,
        )
        # TODO: Может быть, переименовать поврежденный файл?
        return []
    except Exception as e:
        logger.error(
            f"Неожиданная ошибка загрузки истории из {HISTORY_FILE}: {e}", exc_info=True
        )
        return []


def save_history(messages_to_save: list):
    """Сохраняет ПОЛНУЮ историю сообщений в файл JSON."""
    logger.debug(f"Сохранение {len(messages_to_save)} сообщений в {HISTORY_FILE}")
    try:
        # Убедимся, что директория существует (хотя она создается при старте)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(messages_to_save, f, indent=2, ensure_ascii=False)
        logger.info(
            f"История ({len(messages_to_save)} сообщений) успешно сохранена в {HISTORY_FILE}."
        )
    except Exception as e:
        logger.error(f"Ошибка сохранения истории в {HISTORY_FILE}: {e}", exc_info=True)


# --- Импорт утилит ---
try:
    from assistant.utils.summarizer import call_gemini_flash as call_gemini_for_summary
except ImportError:
    logger.error(
        "Не удалось импортировать call_gemini_flash из utils.summarizer. Суммаризация не будет работать."
    )

    def call_gemini_for_summary(*args, **kwargs):
        return None
# --- Конец импорта утилит ---

# --- Константы для Суммаризации (можно переопределить через env) ---
SUMMARY_THRESHOLD = int(os.environ.get("O3_SUMMARY_THRESHOLD", 20))
SUMMARY_BATCH = int(
    os.environ.get("O3_SUMMARY_BATCH", 10)
)  # Кол-во старых сообщений для саммари
KEEP_RECENT = int(
    os.environ.get("O3_KEEP_RECENT", 10)
)  # Кол-во новых сообщений для сохранения
logger.info(
    f"Параметры суммаризации: THRESHOLD={SUMMARY_THRESHOLD}, BATCH={SUMMARY_BATCH}, KEEP_RECENT={KEEP_RECENT}"
)
# --- Конец Констант для Суммаризации ---

# --- Инициализация Контекста для API ---
SYSTEM_PROMPT_CONTENT = (
    "You are a helpful assistant. Use the available tools when appropriate.\n"
    "- 'ask': Consults the Lead Software Engineer (simulated) for high-level advice, plans, or questions about project structure. It has context of the project files.\n"
    "- 'execute_terminal_command': Runs shell commands in the current working directory (CWD). Use carefully for simple tasks like `ls`, `cat`, etc.\n"
    "- 'create_file': Creates or overwrites a file in the CWD.\n"
    "- 'apply_diff': Applies a patch/diff to an existing file in the CWD.\n"
    "- 'query_perplexity': Queries Perplexity AI for research, code examples, best practices, or external information. Use this when information is likely outside the current project."  # Добавлено
)

# Глобальная переменная для истории сообщений
messages = []
# --- Конец Инициализации Контекста ---

# --- Обработка инструментов (пример для 'ask') ---


def ask_tool_backend(query: str):
    """Бэкенд-функция для вызова инструмента 'ask'."""
    logger.info(f"Вызов ask_tool_backend с query: '{query[:50]}...'")
    # Динамический импорт, чтобы избежать тяжелых зависимостей при старте
    try:
        from assistant.tools.ask import handle_ask

        # Передаем API ключ и модель из конфигурации
        return handle_ask(
            query=query, api_key=config.GEMINI_API_KEY, model_name=config.MODEL_ASK
        )
    except ImportError as e:
        logger.error(f"Ошибка импорта handle_ask: {e}", exc_info=True)
        return {
            "status": "error",
            "message": "Ask tool backend not found or import error.",
        }
    except Exception as e:
        logger.error(f"Ошибка выполнения handle_ask: {e}", exc_info=True)
        return {"status": "error", "message": f"Error executing ask tool: {e}"}


# --- Главная функция CLI ---
@click.command()
@click.option(
    "--plain", is_flag=True, help="Disable Rich formatting and advanced input."
)
@click.option(
    "--editor", is_flag=True, help="Use external editor ($EDITOR) for multiline input."
)
@click.option("--user-arg", default="default_value", help="Example custom argument.")
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Enable INFO level logging to console.",
)
@click.version_option(__version__)
def main(plain, editor, user_arg, verbose):
    """Основная функция CLI."""
    # --- Настройка Логирования (вызывается ПЕРЕД чем-либо еще) ---
    setup_logging(verbose=verbose)
    logger.info(f"Platform AI Assistant CLI v{__version__} started. PID: {os.getpid()}")
    logger.debug(
        f"Rich available: {rich_available}, Prompt toolkit available: {prompt_toolkit_available}"
    )
    logger.debug(
        f"CLI args: plain={plain}, editor={editor}, user_arg={user_arg}, verbose={verbose}"
    )
    logger.info(f"Current working directory: {CWD}")
    logger.info(f"History file: {HISTORY_FILE}")
    logger.info(f"Log file: {cli_log_file}")

    # --- Проверка ключей API (после инициализации конфига) ---
    required_keys = {
        "OpenAI": config.OPENAI_API_KEY,
        "Gemini": config.GEMINI_API_KEY,  # Assuming you have this in config
        "Perplexity": config.PERPLEXITY_API_KEY,  # Assuming you have this in config
    }
    missing_keys = [name for name, key in required_keys.items() if not key]

    if missing_keys:
        error_message = f"Required API key(s) missing in environment or .env file: {', '.join(missing_keys)}"
        logger.critical(error_message)
        print(f"\n💥 {error_message}", file=sys.stderr)
        print(
            "Please set them as environment variables or in a .env file.",
            file=sys.stderr,
        )
        sys.exit(1)
    else:
        logger.info("All required API keys found.")

    # --- Инициализация клиента OpenAI (теперь безопасно) ---
    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        logger.info("OpenAI client initialized successfully.")
    except Exception as e:
        logger.critical(
            f"Critical error initializing OpenAI client: {e}", exc_info=True
        )
        print(f"\n💥 Error initializing OpenAI client: {e}", file=sys.stderr)
        sys.exit(1)

    # --- Подготовка к циклу ---
    use_rich = rich_available and not plain
    use_editor = editor
    if use_editor and not os.getenv("EDITOR"):
        logger.warning(
            "Editor mode requested but $EDITOR environment variable is not set. Falling back."
        )
        print(
            "Warning: --editor flag used, but $EDITOR environment variable is not set. Falling back to standard input.",
            file=sys.stderr,
        )
        use_editor = False

    # Сообщаем пользователю о режиме работы
    wrap_print(
        f"Assistant CLI v{__version__}. Rich: {use_rich}. Editor: {use_editor}. Logging to: {cli_log_file}",
        role="system",
    )
    wrap_print(
        "Enter your message below. Use /quit or Ctrl+C/Ctrl+D to exit.", role="system"
    )

    # ❶ Загружаем историю сообщений или создаем пустую
    messages = load_history()
    if not messages:
        # Добавляем системную инструкцию, если история пуста
        messages.append(
            {"role": "system", "content": "You are a helpful AI assistant."}
        )
        logger.info("Initialized new conversation history with system prompt.")
    else:
        logger.info(f"Loaded {len(messages)} messages from history.")

    # ❹ Основной цикл программы
    while True:
        try:
            # Получаем ввод пользователя
            wrap_print("Enter your message:", role="user")  # Prompt for input
            user_input = get_multiline(
                prompt_str="",  # Use empty prompt, wrap_print handles it
                use_editor=use_editor,
                use_prompt_toolkit=use_rich,  # Use rich flag to control prompt_toolkit
            )

            # Проверяем на команду выхода или отмену (Ctrl+C/Ctrl+D)
            if user_input is None:
                logger.info("User cancelled input (Ctrl+C/Ctrl+D). Exiting.")
                wrap_print("Exiting on user request.", role="system")
                break  # Break the loop instead

            user_input_lower = user_input.strip().lower()
            if user_input_lower == "/quit":
                logger.info("User entered /quit. Exiting.")
                wrap_print("Exiting on user request.", role="system")
                break  # Выход из цикла

            if not user_input.strip():
                logger.warning("User entered empty input. Skipping.")
                continue  # Пропускаем пустой ввод

            # Логируем и добавляем сообщение пользователя в историю
            logger.info(f"User input: {user_input[:100]}...")  # Log truncated input
            messages.append({"role": "user", "content": user_input})

            # --- Вызов API ---
            # ❺ Вызываем API с историей сообщений и инструментами
            logger.debug(
                f"Calling OpenAI API with {len(messages)} messages. Tools: {len(TOOLS)}. Choice: {TOOL_CHOICE}"
            )
            logger.debug(f"Messages sent: {messages}")  # Log full message history

            try:
                api_response = client.chat.completions.create(
                    model="gpt-4o",  # Используем последнюю доступную модель
                    messages=messages,
                    tools=TOOLS,
                    tool_choice=TOOL_CHOICE,
                    # max_tokens=150, # Опционально: ограничить длину ответа
                )
                logger.debug(f"API Response received: {api_response}")

                # ❻ Получаем ответ модели
                response_message = api_response.choices[0].message
                tool_calls = (
                    response_message.tool_calls
                )  # ❼ Проверяем, есть ли вызовы инструментов

                # ❽ Если есть вызовы инструментов:
                if tool_calls:
                    # Не добавляем исходный ответ модели с tool_calls в историю
                    # Мы добавим tool_calls и их результаты позже
                    logger.info(f"Assistant requested {len(tool_calls)} tool call(s).")

                    # Копируем историю ДО добавления результатов инструментов
                    # Это важно, так как ответ модели ссылается на эту историю
                    messages_before_tool_results = copy.deepcopy(messages)
                    messages_before_tool_results.append(
                        response_message
                    )  # Add assistant msg with tool calls

                    # ❾ Обрабатываем каждый вызов инструмента
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_args_raw = tool_call.function.arguments
                        tool_call_id = tool_call.id
                        logger.info(
                            f"Processing tool call ID: {tool_call_id}, Function: {function_name}, Args: {function_args_raw}"
                        )

                        # --- Логика вызова бэкенда инструмента ---
                        tool_response_content = None
                        tool_backend_function = None

                        try:
                            # Парсим аргументы JSON
                            function_args = json.loads(function_args_raw)

                            # Определяем, какой бэкенд вызвать
                            if function_name == "ask":
                                tool_backend_function = ask_tool_backend
                            elif function_name == "execute_terminal_command":
                                tool_backend_function = execute_terminal_command
                            elif function_name == "create_file":
                                tool_backend_function = (
                                    handle_create_file  # Use wrapper
                                )
                            elif function_name == "apply_diff":
                                tool_backend_function = handle_apply_diff  # Use wrapper
                            elif function_name == "query_perplexity":
                                tool_backend_function = query_perplexity  # Use wrapper

                            # Если нашли соответствующую функцию
                            if tool_backend_function:
                                # *** Сообщаем пользователю о вызове ***
                                wrap_print(
                                    f"Calling tool `{function_name}` with args: {function_args_raw}",
                                    role="tool_call",
                                )

                                # Вызываем бэкенд-функцию
                                tool_result = tool_backend_function(**function_args)
                                logger.debug(
                                    f"Raw tool result for '{function_name}': {tool_result} (Type: {type(tool_result)})"
                                )

                                # --- Обработка результата инструмента ---
                                # Проверяем тип результата и извлекаем строку для API
                                if isinstance(tool_result, tuple):
                                    # Обрабатываем кортежи от create_file / apply_diff
                                    # (ok: bool, msg: str, diff?: Optional[str])
                                    # Мы хотим отправить только 'msg' обратно в API
                                    tool_response_content = tool_result[
                                        1
                                    ]  # Берем второй элемент - сообщение
                                    # Оригинальное логгирование полного кортежа уже есть выше
                                elif isinstance(tool_result, dict):
                                    # Для execute_terminal_command или других, возвращающих dict
                                    tool_response_content = json.dumps(
                                        tool_result
                                    )  # Преобразуем dict в JSON-строку
                                elif isinstance(tool_result, str):
                                    tool_response_content = tool_result
                                else:
                                    # Неожиданный тип - логируем и преобразуем в строку
                                    logger.warning(
                                        f"Unexpected result type from tool '{function_name}': {type(tool_result)}. Converting to string."
                                    )
                                    tool_response_content = str(tool_result)

                                # *** Сообщаем пользователю о завершении ***
                                wrap_print(
                                    f"✓ `{function_name}` finished.",
                                    role="tool_response",
                                )

                            else:
                                logger.error(
                                    f"Error: Function '{function_name}' not found."
                                )
                                tool_response_content = f'{{"error": "Function {function_name} not found."}}'
                                wrap_print(
                                    f"Error: Tool `{function_name}` not found.",
                                    role="system",
                                )  # Inform user

                        except json.JSONDecodeError as e:
                            logger.error(
                                f"Error decoding JSON arguments for {function_name}: {e}\\nArguments: {function_args_raw}",
                                exc_info=True,
                            )
                            tool_response_content = (
                                f'{{"error": "Invalid JSON arguments: {e}"}}'
                            )
                            wrap_print(
                                f"Error decoding arguments for `{function_name}`.",
                                role="system",
                            )
                        except TypeError as e:
                            # Ловим ошибки, если аргументы не соответствуют сигнатуре функции
                            logger.error(
                                f"TypeError calling tool backend '{function_name}' with args {function_args}: {e}",
                                exc_info=True,
                            )
                            tool_response_content = f'{{"error": "TypeError calling backend function: {e}"}}'
                            wrap_print(
                                f"Error calling tool `{function_name}`: {e}",
                                role="system",
                            )
                        except Exception as e:
                            # Общий обработчик ошибок при вызове бэкенда
                            logger.error(
                                f"Error executing tool backend '{function_name}' with args {function_args_raw}: {e}",
                                exc_info=True,
                            )
                            tool_response_content = (
                                f'{{"error": "Error executing tool: {e}"}}'
                            )
                            wrap_print(
                                f"Error during `{function_name}` execution: {e}",
                                role="system",
                            )

                        # ❿ Добавляем результат вызова инструмента в историю для следующего шага
                        # Используем ИСХОДНУЮ историю (messages_before_tool_results)
                        messages_before_tool_results.append(
                            {
                                "tool_call_id": tool_call_id,
                                "role": "tool",
                                "name": function_name,
                                "content": tool_response_content,  # Отправляем извлеченную строку
                            }
                        )
                        logger.debug(
                            f"Appended tool result for {tool_call_id} to temporary history."
                        )

                    # ⓫ Вызываем API еще раз, предоставив результаты инструментов
                    logger.info("Calling API again with tool results.")
                    logger.debug(
                        f"Messages with tool results: {messages_before_tool_results}"
                    )
                    second_api_response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages_before_tool_results,  # Передаем историю с результатами
                    )
                    logger.debug(f"Second API response: {second_api_response}")

                    # Получаем финальный ответ модели после обработки инструментов
                    final_response_message = second_api_response.choices[0].message
                    messages.append(
                        response_message
                    )  # Добавляем исходное сообщение ассистента с tool_calls
                    # Добавляем все сообщения tool из временной истории
                    for msg in messages_before_tool_results:
                        if msg["role"] == "tool":
                            messages.append(msg)
                    messages.append(final_response_message)  # Добавляем финальный ответ
                    assistant_response_content = final_response_message.content
                    logger.info("Assistant final response after tool use.")

                # ⓬ Если вызовов инструментов не было, просто берем ответ модели
                else:
                    assistant_response_content = response_message.content
                    messages.append(
                        response_message
                    )  # Добавляем ответ ассистента в историю
                    logger.info("Assistant response received (no tool calls).")

                # --- Вывод ответа ассистента ---
                if assistant_response_content:
                    wrap_print(assistant_response_content, role="assistant")
                    logger.debug(
                        f"Assistant response content: {assistant_response_content[:100]}..."
                    )
                else:
                    # Случай, когда нет ни контента, ни tool calls (маловероятно, но возможно)
                    logger.warning(
                        "Assistant response was empty (no content or tool calls)."
                    )
                    wrap_print("[Assistant provided an empty response]", role="system")

            except Exception as e:
                logger.error(f"Error during API call or processing: {e}", exc_info=True)
                # wrap_print(f"An error occurred: {e}", "error") # Or use system role
                wrap_print(
                    f"An error occurred: {e}", role="system"
                )  # Using system role for errors

        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt received. Exiting.")
            wrap_print("Exiting on user request.", role="system")
            break
        except EOFError:  # Обработка Ctrl+D в некоторых терминалах
            logger.info("EOFError received (Ctrl+D). Exiting.")
            wrap_print("Exiting on user request.", role="system")
            break

    # --- Завершение ---
    save_history(messages)  # Сохраняем историю при выходе
    logger.info("Exiting CLI application. History saved.")


def _format_tool_result_for_print(
    tool_name: str, tool_result: dict | str, tool_args: str
) -> str:
    """Форматирует результат инструмента для вывода в консоль."""
    result_str = ""
    # ... (остальная часть функции без изменений)
    return result_str


# --- Функции-обертки для бэкендов инструментов ---
# Эти функции запускают скрипты в подпроцессах


def handle_create_file(target_file: str, content: str) -> Tuple[bool, str]:
    """Вызывает file_modifier.py create и возвращает (success, message)."""
    script_path = Path(__file__).parent / "tools" / "file_modifier.py"
    command = [sys.executable, str(script_path), "create", target_file]
    logger.info(f"Executing file modifier: {' '.join(command)}")
    try:
        process = subprocess.run(
            command,
            input=content,
            text=True,
            capture_output=True,
            check=False,  # Don't raise exception on non-zero exit code
            encoding="utf-8",
        )
        logger.debug(f"file_modifier create stdout: {process.stdout}")
        logger.debug(f"file_modifier create stderr: {process.stderr}")

        if process.returncode == 0:
            logger.info(f"File '{target_file}' created/overwritten successfully.")
            # Возвращаем stdout как сообщение об успехе
            return (
                True,
                process.stdout.strip() or f"File '{target_file}' created/overwritten.",
            )
        else:
            error_msg = (
                process.stderr.strip()
                or f"Unknown error creating file '{target_file}'."
            )
            logger.error(f"Error creating file '{target_file}': {error_msg}")
            return False, f"Error: {error_msg}"
    except Exception as e:
        logger.exception(f"Failed to run file_modifier create for '{target_file}'")
        return False, f"Failed to execute file creation: {e}"


def handle_apply_diff(
    target_file: str, diff_content: str
) -> Tuple[bool, str, Optional[str]]:
    """Вызывает file_modifier.py apply и возвращает (success, message, actual_diff)."""
    script_path = Path(__file__).parent / "tools" / "file_modifier.py"
    command = [sys.executable, str(script_path), "apply", target_file]
    logger.info(f"Executing file modifier apply: {' '.join(command)}")
    try:
        process = subprocess.run(
            command,
            input=diff_content,
            text=True,
            capture_output=True,
            check=False,
            encoding="utf-8",
        )
        logger.debug(f"file_modifier apply stdout: {process.stdout}")
        logger.debug(f"file_modifier apply stderr: {process.stderr}")

        if process.returncode == 0:
            # Diff applied successfully, stdout might contain the actual diff applied
            actual_diff = process.stdout.strip()
            message = f"Changes applied to '{target_file}'."
            logger.info(message)
            return True, message, actual_diff if actual_diff else None
        else:
            error_msg = (
                process.stderr.strip()
                or f"Unknown error applying diff to '{target_file}'."
            )
            logger.error(f"Error applying diff to '{target_file}': {error_msg}")
            return False, f"Error: {error_msg}", None
    except Exception as e:
        logger.exception(f"Failed to run file_modifier apply for '{target_file}'")
        return False, f"Failed to execute diff application: {e}", None


def query_perplexity_backend(
    query: str, attachments: Optional[List[str]] = None
) -> str:
    """Вызывает perplexity_tool.py и возвращает ответ."""
    script_path = Path(__file__).parent / "tools" / "perplexity_tool.py"
    command = [sys.executable, str(script_path)]
    if attachments:
        for attachment in attachments:
            command.extend(["--attach", attachment])
    command.extend(["--query", query])  # Add query last

    logger.info(
        f"Executing Perplexity tool: {' '.join(shlex.quote(c) for c in command)}"
    )
    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,  # Raise exception on non-zero exit
            encoding="utf-8",
        )
        logger.debug(
            f"Perplexity tool stdout: {process.stdout[:200]}..."
        )  # Log truncated output
        return process.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_msg = f"Error executing Perplexity tool: {e}. Stderr: {e.stderr.strip()}"
        logger.error(error_msg)
        return f'{{"error": "{error_msg}"}}'  # Return error as JSON string
    except Exception as e:
        logger.exception("Failed to run Perplexity tool script")
        return f'{{"error": "Failed to execute Perplexity tool script: {e}"}}'


if __name__ == "__main__":
    main()
