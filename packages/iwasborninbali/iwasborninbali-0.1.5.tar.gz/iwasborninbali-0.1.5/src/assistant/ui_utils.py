import sys
from typing import Optional

_rich_available = False
_console = None

try:
    from rich.console import Console
    from rich.panel import Panel

    _console = Console()
    _rich_available = True
except ImportError:
    pass  # Rich не установлен, будем использовать обычный print


def wrap_print(text: str, *, role: Optional[str] = None, **kwargs):
    """Выводит текст, опционально оборачивая его в панель Rich, используя 'role' для стилизации."""
    use_rich = _rich_available  # rich_enabled was always True

    # Default role if not provided
    role = role or "assistant"  # Default to assistant styling if role is None

    if use_rich and _console:
        title = "Assistant"  # Default title
        color = "green"  # Default color

        if role == "user":
            title = "You"
            color = "blue"
        elif role == "assistant":
            # Defaults already set
            pass
        # Заменяем маркеры у tool calls для лучшего вида в панели
        elif role == "tool_call":
            title = "Tool Call"
            color = "cyan"
            # text remains unchanged for tool call/response in rich mode
        elif role == "tool_response":
            title = "Tool Response"
            color = "green"
            # text remains unchanged
        elif role == "system":
            title = "System"
            color = "yellow"
        # else: role is something else, use defaults

        try:
            _console.print(Panel(text, title=title, border_style=color, expand=False))
        except Exception as e:
            # Если вывод через Rich не удался, откатываемся к print
            print(f"Error using Rich: {e}", file=sys.stderr)
            plain_print(role, text)

    else:
        plain_print(role, text)


def plain_print(role: str, text: str):
    """Простой вывод текста с префиксом роли."""
    if role == "user":
        print(f"You: {text}")
    elif role == "assistant":
        print(f"\n💬 Assistant:\n{text}")
    elif role == "tool_call":
        # Возвращаем стрелку для plain режима
        print(f">> {text}")
    elif role == "tool_response":
        # Возвращаем стрелку
        print(f"✓ {text}")
    else:  # system, tool?
        print(f"[{role.upper()}]: {text}")


# Экспортируем флаг доступности Rich
rich_available = _rich_available
