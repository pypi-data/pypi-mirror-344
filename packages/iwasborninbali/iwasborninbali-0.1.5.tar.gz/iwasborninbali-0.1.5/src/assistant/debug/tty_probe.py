import sys
import os
import tty
import termios
import atexit
import time  # Добавляем для небольшой паузы

original_termios_settings = None


def restore_terminal():
    """Restores the terminal settings on exit."""
    global original_termios_settings
    if original_termios_settings:
        print("\n[DEBUG] Attempting to restore terminal settings...")
        try:
            termios.tcsetattr(
                sys.stdin.fileno(), termios.TCSADRAIN, original_termios_settings
            )
            print("[INFO] Terminal settings restored.")
        except Exception as e:
            print(f"[ERROR] Failed to restore terminal settings: {e}")
    else:
        print("\n[DEBUG] No original termios settings found to restore.")


def main():
    global original_termios_settings
    if not sys.stdin.isatty():
        print("Error: This script requires running from a TTY.", file=sys.stderr)
        sys.exit(1)

    print("--- TTY Raw Input Probe --- (for debugging input issues)")
    print("Instructions:")
    print("1. Type or paste the text that causes input problems.")
    print("2. Press Ctrl+D when you are finished (or when input truncates).")
    print("3. The script will print the raw bytes received as a hex dump.")
    print(
        "4. Copy the *entire* hex dump and report it, along with where the input stopped."
    )
    print("\nStarting raw input capture (press Ctrl+D to finish)...")

    # Store original settings and register restoration hook
    try:
        original_termios_settings = termios.tcgetattr(sys.stdin.fileno())
        print("[DEBUG] Original termios settings stored.")
        atexit.register(restore_terminal)
        print("[DEBUG] atexit handler registered.")
    except Exception as e:
        print(
            f"[ERROR] Failed to get/store initial terminal settings: {e}",
            file=sys.stderr,
        )
        sys.exit(1)

    all_bytes = bytearray()
    try:
        # Set terminal to raw mode
        tty.setraw(sys.stdin.fileno())
        print("[DEBUG] Terminal set to raw mode.")

        read_iterations = 0
        while True:
            read_iterations += 1
            print(f"\n[DEBUG Iteration {read_iterations}] Waiting for os.read()...")
            try:
                chunk = os.read(sys.stdin.fileno(), 1024)
                print(
                    f"[DEBUG Iteration {read_iterations}] os.read() returned: {chunk!r} (length: {len(chunk)})"
                )

                if not chunk:  # EOF detected (Ctrl+D should return b'')
                    print(
                        "\n[DEBUG] EOF detected (empty chunk received). Breaking loop."
                    )
                    break

                all_bytes.extend(chunk)
                print(
                    f"[DEBUG Iteration {read_iterations}] Total bytes collected: {len(all_bytes)}"
                )
                # Небольшая пауза, чтобы вывод успел отобразиться
                time.sleep(0.01)

            except OSError as e:
                print(f"\n[ERROR] Read error in loop: {e}", file=sys.stderr)
                break
            except KeyboardInterrupt:
                print("\n[INFO] KeyboardInterrupt received, finishing capture...")
                break

    finally:
        print("\n[DEBUG] Exiting read loop / entering finally block.")
        # Ensure terminal is restored even if errors occur before atexit
        restore_terminal()
        # Clear the global to prevent double restoration by atexit if called manually
        original_termios_settings = None

    print("\n--- Input Capture Finished --- (Outside loop)")
    print(f"Total bytes received: {len(all_bytes)}")
    print("Hex dump of received bytes:")
    try:
        hex_dump = all_bytes.hex()
        print(hex_dump)
    except Exception as e:
        print(f"[ERROR] Failed to generate hex dump: {e}")
    print("-----------------------------")
    print("[DEBUG] End of main function.")


if __name__ == "__main__":
    main()
