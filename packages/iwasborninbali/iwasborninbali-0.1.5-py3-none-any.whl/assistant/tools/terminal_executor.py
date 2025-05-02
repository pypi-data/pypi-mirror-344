import subprocess
import json
import select  # Added for non-blocking read
import time  # Added for sleep
import os  # Added for os.getcwd()
import shlex  # For safer command splitting
import threading  # To check the interrupt event
import logging  # Added for logging

# Настройка логгера для этого модуля
logger = logging.getLogger(__name__)
# Путь к логам теперь берем относительно CWD, предполагая, что cli.py создал папку logs
# CWD = Path.cwd()
# LOGS_DIR = CWD / 'logs' # Не можем использовать CWD из cli.py напрямую
# Вместо этого, пусть cli.py передает путь через env или параметр, или используем относительный путь от корня пакета
# Пока самый простой вариант - использовать logging без файла,
# пусть основной logger из cli.py перехватывает сообщения.
# Если нужно писать в отдельный файл, потребуется передать LOGS_DIR.
# logging.basicConfig(level=logging.DEBUG) # Убираем настройку файла здесь

MAX_OUTPUT_BYTES = 1024 * 1024  # 1MB limit for stdout/stderr capture
# TRIM_KEEP_BYTES = 4096 # Bytes to keep from head and tail when trimming - Removed, simple truncation now
POLL_INTERVAL = 0.1  # Seconds to wait between checking process status/interrupt
READ_CHUNK_SIZE = 4096  # Bytes to read at a time from streams

# Default return structure for errors before process starts
DEFAULT_ERROR_RETURN = {
    "status": "error",
    "exit_code": None,
    "stdout": "",
    "stderr": "",
    "truncated": False,
}


def _read_stream(stream, buffer: list[bytes], limit: int) -> bool:
    """
    Reads from a non-blocking stream into a buffer list, strictly respecting the byte limit.
    Returns True if the output was truncated during this read operation.
    """
    truncated_in_this_call = False
    try:
        while True:
            # Calculate remaining capacity *before* reading
            current_bytes_in_buffer = sum(len(c) for c in buffer)
            remaining_capacity = limit - current_bytes_in_buffer

            if remaining_capacity <= 0:
                # Buffer is already full or over limit, cannot read more
                # Check if there might be more data in the stream to mark as truncated
                ready_to_read, _, _ = select.select(
                    [stream], [], [], 0
                )  # Non-blocking check
                if ready_to_read:
                    truncated_in_this_call = True
                    logger.warning(
                        f"Stream reading stopped; buffer full ({current_bytes_in_buffer}/{limit} bytes). Potential truncation."
                    )
                break  # Stop reading

            # Determine max bytes to read in this chunk
            read_size = min(READ_CHUNK_SIZE, remaining_capacity)
            chunk = os.read(stream.fileno(), read_size)

            if not chunk:
                break  # End of stream

            buffer.append(chunk)
            # No need to update total_bytes here, calculated at loop start

            # If we read less than requested, it might be EOF or just temporary pause
            # If we read exactly up to the remaining capacity, and there might be more data, we truncated
            if len(chunk) == read_size and remaining_capacity - len(chunk) == 0:
                # We filled the buffer exactly. Check if more data is waiting.
                ready_to_read, _, _ = select.select(
                    [stream], [], [], 0
                )  # Non-blocking check
                if ready_to_read:
                    truncated_in_this_call = True
                    logger.warning(
                        f"Stream reading stopped; hit limit ({limit} bytes) exactly. Potential truncation."
                    )
                    break  # Stop reading

    except (BlockingIOError, InterruptedError):
        pass  # Expected when reading non-blocking streams
    except (BrokenPipeError, OSError) as e:
        logger.debug(f"Error reading stream (potentially closed): {e}")
        pass
    except Exception as e:
        logger.error(f"Unexpected error reading stream: {e}", exc_info=True)
        # Consider if truncation should be True here, depends on desired behavior

    # Final check after loop: if buffer is at limit and flag wasn't set, check stream again
    if not truncated_in_this_call and sum(len(c) for c in buffer) >= limit:
        ready_to_read, _, _ = select.select([stream], [], [], 0)
        if ready_to_read:
            truncated_in_this_call = True
            logger.warning(
                f"Stream reading finished, but buffer is full ({sum(len(c) for c in buffer)}/{limit} bytes) and more data might exist. Marking truncated."
            )

    return truncated_in_this_call


def handle_terminal_command(
    json_string: str, base_cwd: str, interrupt_event: threading.Event
) -> dict:
    """Executes a terminal command using Popen, allowing for interruption. Returns JSON-serializable dict."""
    try:
        payload = json.loads(json_string)
        command_str = payload.get("command")
        stdin_payload = payload.get("stdin")
    except json.JSONDecodeError as e:
        return {**DEFAULT_ERROR_RETURN, "error_message": f"Invalid JSON payload: {e}"}
    except AttributeError:  # Handle if payload is not dict-like
        return {
            **DEFAULT_ERROR_RETURN,
            "error_message": "Invalid payload structure (not a dictionary?)",
        }

    if not command_str:
        return {**DEFAULT_ERROR_RETURN, "error_message": "Missing 'command' in payload"}

    # Use shlex to split command safely
    try:
        command_parts = shlex.split(command_str)
        if not command_parts:
            return {
                **DEFAULT_ERROR_RETURN,
                "error_message": "Empty command after parsing",
            }
    except ValueError as e:
        return {**DEFAULT_ERROR_RETURN, "error_message": f"Error parsing command: {e}"}

    # Use logger instead of print for internal messages
    logger.info(f"Executing command: {' '.join(command_parts)}")
    logger.info(f"Working directory: {base_cwd}")

    process = None
    stdout_truncated = False
    stderr_truncated = False
    try:
        process = subprocess.Popen(
            command_parts,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=base_cwd,
            text=False,  # Work with bytes
            bufsize=0,  # Unbuffered
        )

        stdout_buffer = []
        stderr_buffer = []

        # Set streams to non-blocking
        os.set_blocking(process.stdout.fileno(), False)
        os.set_blocking(process.stderr.fileno(), False)

        # Write stdin if provided
        if stdin_payload:
            try:
                process.stdin.write(stdin_payload.encode("utf-8", errors="ignore"))
                process.stdin.close()
            except OSError as e:
                logger.warning(f"Could not write to stdin: {e}")  # Log warning

        # Poll for completion and check interrupt flag
        while process.poll() is None:
            if interrupt_event.is_set():
                logger.info("Interrupt signal detected. Terminating command.")
                try:
                    process.terminate()
                    process.wait(timeout=0.5)
                except subprocess.TimeoutExpired:
                    logger.warning("Process did not terminate gracefully. Killing.")
                    process.kill()
                except Exception as term_err:
                    logger.error(f"Error during process termination: {term_err}")

                # Read remaining output after trying to terminate
                stdout_truncated = (
                    _read_stream(process.stdout, stdout_buffer, MAX_OUTPUT_BYTES)
                    or stdout_truncated
                )
                stderr_truncated = (
                    _read_stream(process.stderr, stderr_buffer, MAX_OUTPUT_BYTES)
                    or stderr_truncated
                )

                stdout_bytes = b"".join(stdout_buffer)
                stderr_bytes = b"".join(stderr_buffer)
                stdout_str = stdout_bytes.decode(
                    "utf-8", errors="replace"
                )  # Use replace on final decode
                stderr_str = stderr_bytes.decode("utf-8", errors="replace")

                # Return error status for interruption
                return {
                    "status": "error",
                    "exit_code": process.poll(),
                    "error_message": "Command interrupted by user.",
                    "stdout": stdout_str,  # Return the (potentially truncated) string
                    "stderr": stderr_str,
                    "truncated": stdout_truncated
                    or stderr_truncated,  # Use the flag from _read_stream
                }

            # Read available output without blocking
            stdout_read_truncated = _read_stream(
                process.stdout, stdout_buffer, MAX_OUTPUT_BYTES
            )
            stderr_read_truncated = _read_stream(
                process.stderr, stderr_buffer, MAX_OUTPUT_BYTES
            )
            stdout_truncated = stdout_truncated or stdout_read_truncated
            stderr_truncated = stderr_truncated or stderr_read_truncated

            time.sleep(POLL_INTERVAL)

        # Process finished normally, read any final output
        stdout_read_truncated = _read_stream(
            process.stdout, stdout_buffer, MAX_OUTPUT_BYTES
        )
        stderr_read_truncated = _read_stream(
            process.stderr, stderr_buffer, MAX_OUTPUT_BYTES
        )
        stdout_truncated = stdout_truncated or stdout_read_truncated
        stderr_truncated = stderr_truncated or stderr_read_truncated

        exit_code = process.returncode
        # Decode final output using replace
        stdout_bytes = b"".join(stdout_buffer)
        stderr_bytes = b"".join(stderr_buffer)
        stdout_str = stdout_bytes.decode("utf-8", errors="replace")
        stderr_str = stderr_bytes.decode("utf-8", errors="replace")

        logger.info(f"Command finished with exit code: {exit_code}")
        logger.info(
            f"Output captured - stdout: {len(stdout_bytes)} bytes (truncated: {stdout_truncated}), stderr: {len(stderr_bytes)} bytes (truncated: {stderr_truncated})"
        )

        final_truncated_flag = stdout_truncated or stderr_truncated

        if exit_code == 0:
            return {
                "status": "success",
                "exit_code": exit_code,
                "stdout": stdout_str,  # Return final string
                "stderr": stderr_str,
                "truncated": final_truncated_flag,  # Report final flag
            }
        else:
            return {
                "status": "error",
                "exit_code": exit_code,
                "error_message": f"Command failed with exit code {exit_code}",
                "stdout": stdout_str,
                "stderr": stderr_str,
                "truncated": final_truncated_flag,
            }

    except FileNotFoundError:
        logger.error(f"Command not found: {command_parts[0]}")
        return {
            **DEFAULT_ERROR_RETURN,
            "error_message": f"Command not found: {command_parts[0]}",
        }
    except Exception as e:
        logger.error(f"Failed to execute command: {e}", exc_info=True)  # Log traceback
        # Ensure process is cleaned up
        if process and process.poll() is None:
            logger.info(f"Cleaning up process {process.pid} due to exception: {e}")
            try:
                process.kill()
            except Exception as kill_err:
                logger.error(f"Error during cleanup kill: {kill_err}")

        # Try to capture stderr from the exception itself if possible
        stderr_from_exception = str(e)
        return {
            **DEFAULT_ERROR_RETURN,
            "error_message": f"Failed to execute command: {e}",
            "stderr": stderr_from_exception,
        }
    finally:
        # Ensure pipes are closed
        if process:
            for stream in [process.stdin, process.stdout, process.stderr]:
                if stream:
                    try:
                        stream.close()
                    except OSError as e:
                        logger.debug(f"Error closing stream: {e}")  # Log debug message
            try:
                process.wait(timeout=0.1)  # Final check for zombies
            except subprocess.TimeoutExpired:
                logger.warning(
                    f"Process {process.pid} did not exit cleanly after handling."
                )
            except Exception as wait_err:
                logger.debug(f"Error during final process wait: {wait_err}")


# Wrapper function for simpler direct calls if needed (though handle_terminal_command is primary)
# Keeping execute_terminal_command for potential future use or compatibility,
# but ensuring it also returns the standard JSON structure.
def execute_terminal_command(
    command: str,
    stdin: str | None = None,
    cwd: str | None = None,
    interrupt_event: threading.Event = None,
) -> dict:
    """Выполняет команду терминала, возвращает JSON-совместимый словарь."""
    if interrupt_event is None:
        interrupt_event = threading.Event()  # Create dummy if not provided

    # Prepare JSON payload for handle_terminal_command
    payload = {"command": command}
    if stdin is not None:
        payload["stdin"] = stdin

    json_payload = json.dumps(payload)
    effective_cwd = cwd or os.getcwd()  # Use provided cwd or current working directory

    # Call the main handler function
    result = handle_terminal_command(
        json_string=json_payload,
        base_cwd=effective_cwd,
        interrupt_event=interrupt_event,
    )
    return result


# Example Usage (for testing purposes)
if __name__ == "__main__":
    test_event = threading.Event()

    # Test 1: Simple command
    print("--- Test 1: Simple command ---")
    result1 = execute_terminal_command(
        command="echo 'Hello World!'", interrupt_event=test_event
    )
    print(json.dumps(result1, indent=2))

    # Test 2: Command with stderr
    print("\n--- Test 2: Command with stderr ---")
    result2 = execute_terminal_command(
        command="ls non_existent_file", interrupt_event=test_event
    )
    print(json.dumps(result2, indent=2))

    # Test 3: Command with stdin
    print("\n--- Test 3: Command with stdin ---")
    result3 = execute_terminal_command(
        command="grep test",
        stdin="This is a test line\nAnother line",
        interrupt_event=test_event,
    )
    print(json.dumps(result3, indent=2))

    # Test 4: Long running command (interrupt manually within ~5s if needed for testing interrupt)
    # print("\n--- Test 4: Long running command (interrupt test) ---")
    # long_cmd_thread = threading.Thread(target=execute_terminal_command, args=("sleep 10", None, None, test_event))
    # long_cmd_thread.start()
    # time.sleep(2)
    # print("Setting interrupt event...")
    # test_event.set()
    # long_cmd_thread.join()
    # print("Interrupt test finished.") # Result will be printed by the thread, check logs too

    # Test 5: Truncation test
    print("\n--- Test 5: Truncation test ---")
    # Generate a lot of output (adjust count as needed)
    # Using head to ensure it terminates even if yes is very fast
    truncate_cmd = "yes | head -c 2M"  # Generate ~2MB
    MAX_OUTPUT_BYTES = 50 * 1024  # Temporarily reduce limit for testing
    result5 = execute_terminal_command(
        command=truncate_cmd, interrupt_event=threading.Event()
    )  # Use fresh event
    print(json.dumps(result5, indent=2))
    print(
        f"Stdout length: {len(result5.get('stdout', ''))}, Stderr length: {len(result5.get('stderr', ''))}"
    )
    MAX_OUTPUT_BYTES = 1024 * 1024  # Restore original limit

    # Test 6: Invalid command
    print("\n--- Test 6: Invalid command ---")
    result6 = execute_terminal_command(
        command="invalid^_^command", interrupt_event=threading.Event()
    )
    print(json.dumps(result6, indent=2))

    # Test 7: Error in JSON payload (passed to handle_terminal_command)
    print("\n--- Test 7: Invalid JSON ---")
    result7 = handle_terminal_command(
        json_string="{invalid json", base_cwd=".", interrupt_event=threading.Event()
    )
    print(json.dumps(result7, indent=2))

    # Test 8: Missing command in payload
    print("\n--- Test 8: Missing command key ---")
    result8 = handle_terminal_command(
        json_string='{"stdin": "test"}', base_cwd=".", interrupt_event=threading.Event()
    )
    print(json.dumps(result8, indent=2))
