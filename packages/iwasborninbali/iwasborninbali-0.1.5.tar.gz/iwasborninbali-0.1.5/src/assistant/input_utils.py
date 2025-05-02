import logging

# Style variable will be defined conditionally
style = None

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import FileHistory

    # from prompt_toolkit.shortcuts import prompt # <<< Remove unused import
    from prompt_toolkit.styles import Style  # Keep import here
    from prompt_toolkit.key_binding import KeyBindings

    prompt_toolkit_available = True

    # Define style ONLY if prompt_toolkit is available
    style = Style.from_dict(
        {
            "": "#ff0066",  # Default text color
            "prompt": "#00aa00",  # Prompt symbol color
        }
    )

    # Define kb ONLY if prompt_toolkit is available
    kb = KeyBindings()

except ImportError:
    prompt_toolkit_available = False

    # style remains None
    # Define dummy kb if prompt_toolkit is not available
    class DummyKeyBindings:
        def add(self, *args, **kwargs):
            def decorator(func):
                return func

            return decorator

    kb = DummyKeyBindings()

try:
    import click  # Добавлен для click.edit

    click_available = True
except ImportError:
    click_available = False

logger = logging.getLogger(__name__)


@kb.add("c-d")
def _(event):
    """Pressing Ctrl+D will end the input."""
    event.app.exit(result=event.cli.current_buffer.text)


def read_from_editor(initial_text: str = "") -> str | None:
    """Opens the default system editor ($EDITOR) to read multiline input.

    Args:
        initial_text (str): Initial text to populate the editor with.

    Returns:
        str | None: The edited text, or None if the editor was closed without changes
                    or if click is unavailable.
    """
    if not click_available:
        logger.error(
            "`click` library is required for editor input. Install with 'pip install platform-ai[ui]'."
        )
        return None

    marker = "# Please enter your message above this line\n# Lines starting with '#' will be ignored.\n"
    message = f"{initial_text}\n\n{marker}"

    try:
        edited_message = click.edit(message)
        if edited_message is not None:
            # Remove the marker and comments
            content = edited_message.split(marker)[0].rstrip("\n")
            lines = content.split("\n")
            # Filter out comment lines
            actual_lines = [line for line in lines if not line.strip().startswith("#")]
            final_text = "\n".join(actual_lines).strip()

            # Check if the final text is unchanged from the initial text (ignoring comments)
            if final_text == initial_text.strip():
                logger.info("Editor closed without changes.")
                return None  # Indicate no change or only comments were present
            return final_text
        else:
            # click.edit returns None if editor could not be opened or exited abnormally
            logger.warning("Editor closed without saving or could not be opened.")
            return None
    except Exception as e:
        logger.error(f"Error using editor: {e}")
        return None


def get_multiline_input_prompt_toolkit(prompt_str=">>> ", history_file=".cli_history"):
    """Get multiline input using prompt_toolkit.
    End input with Ctrl+D or by typing '/end' on a new line.
    """
    session = PromptSession(history=FileHistory(history_file))
    print("(Press Ctrl+D or type '/end' on a new line to send)")
    lines = []
    while True:
        try:
            line = session.prompt(
                prompt_str if not lines else "... ",
                multiline=False,  # Use multiline=False for better control with loop
                wrap_lines=True,
                style=style,
                key_bindings=kb,
                # refresh_interval=0.5 # Optional: for dynamic updates
            )
            # Check for '/end' command AFTER getting the line via prompt
            if line.strip() == "/end":
                break
            lines.append(line)
        except EOFError:  # Ctrl+D was pressed
            break
        except KeyboardInterrupt:  # Ctrl+C
            print("\nInput cancelled.")
            return None
    return "\n".join(lines)


def get_multiline_input_fallback(prompt_str=">>> "):
    """Fallback multiline input using standard input.
    End input with an empty line or by typing '/end'.
    """
    print(f"{prompt_str}(Type '/end' or press Enter on an empty line to send)")
    lines = []
    while True:
        try:
            line = input("... " if lines else "")
            if line.strip() == "/end" or line == "":
                break
            lines.append(line)
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nInput cancelled.")
            return None
    return "\n".join(lines)


def get_multiline(
    prompt_str=">>> ",
    use_prompt_toolkit=True,
    use_editor=False,
    history_file=".cli_history",
):
    """Get multiline user input, optionally using an external editor or prompt_toolkit.

    Args:
        prompt_str (str): The prompt string to display.
        use_prompt_toolkit (bool): Whether to attempt using prompt_toolkit (if not using editor).
        use_editor (bool): If True, open $EDITOR for input. Takes precedence.
        history_file (str): Path to the history file for prompt_toolkit.

    Returns:
        str or None: The user's input as a single string, or None if cancelled/empty.
    """
    if use_editor:
        logger.debug("Using external editor for input.")
        return read_from_editor()

    if use_prompt_toolkit and prompt_toolkit_available:
        logger.debug("Using prompt_toolkit for multiline input.")
        return get_multiline_input_prompt_toolkit(prompt_str, history_file)
    else:
        if use_prompt_toolkit and not prompt_toolkit_available:
            logger.warning("prompt_toolkit not found. Falling back to standard input.")
            logger.warning(
                "Install with 'pip install platform-ai[ui]' for a better experience."
            )
        elif not use_prompt_toolkit:
            logger.debug("Using standard input for multiline input (--plain mode).")
        return get_multiline_input_fallback(prompt_str)
