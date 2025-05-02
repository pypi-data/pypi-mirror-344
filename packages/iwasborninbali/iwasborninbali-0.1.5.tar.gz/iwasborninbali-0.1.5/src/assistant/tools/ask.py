import json
import sys
import requests
import fnmatch
import subprocess
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# --- Configuration (Can be adjusted) ---
ASK_MAX_TOKENS = 100000  # Limit for the response from Gemini
DEFAULT_EXTENSIONS = [
    "md",
    "txt",
    "json",
    "py",
    "js",
    "ts",
    "tsx",
    "jsx",
    "sh",
    "yaml",
    "yml",
    "css",
    "html",
    "Dockerfile",
    "Makefile",
]
DEFAULT_EXCLUDE_DIRS = [
    ".git",
    "node_modules",
    "__pycache__",
    "venv*",
    ".venv",
    ".env*",
    "ask",
    "edit",
    "o3",
    "gemini_history",
    ".ruff_cache",
    ".next",
    "build",
    "dist",
    "*.egg-info",
]
DEFAULT_EXCLUDE_FILES = [
    ".env",
    ".env.local",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "*.log",
    "messages.json",
    "*.pyc",
    "*.swp",
    "*.bk",
    "*.tmp",
]
MAX_FILES_FOR_CONTEXT = 20
MAX_FILE_SIZE_BYTES = 500 * 1024
MAX_CONTEXT_SIZE_BYTES = 500 * 1024
MAX_TREE_LINES = 100
API_TIMEOUT_SECONDS = 180
# --- End Configuration ---

LEAD_ENGINEER_PROMPT = """
You are a Lead Software Engineer. Your goal is to understand the user's request, analyze the provided context (code files, project structure), and provide high-level consultation or create a detailed, step-by-step implementation plan **without any code snippets**.

Instructions:
1.  **Analyze the Request:** Deeply understand the core problem, feature request, or task.
2.  **Consider Context:** Carefully analyze the provided project structure and relevant file contents. How does the request impact existing code?
3.  **Formulate Detailed Plan OR Consultation:**
    *   Outline a clear, step-by-step plan to implement the solution, focusing on the approach, affected components/files, and logical sequence. **Do NOT include any code.** Prioritize clarity and feasibility.
    *   Alternatively, if a plan isn't appropriate, provide high-level consultation, architectural advice, or discuss potential approaches and trade-offs.
    *   Identify potential challenges or considerations.
4.  **Output:** Present the plan or consultation clearly and logically **as plain text, without using any markdown formatting (like **, *, ```, etc.)**. Be concise but thorough.
"""


def call_gemini_for_ask(
    system_prompt: str,
    user_input_with_context: str,
    api_key: str,
    model_name: str,
    max_tokens: int = ASK_MAX_TOKENS,
):
    """Calls the Gemini API with the provided context and handles the response."""
    logger.info(f"Ask Tool: Preparing API call to model: {model_name}")
    if not api_key:
        logger.error("Ask Tool: API Key is missing.")
        return "Error: GEMINI_API_KEY was not provided to the ask tool."

    headers = {"Content-Type": "application/json"}
    # Construct the API endpoint URL dynamically
    # Example format: https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent
    # Assumes model_name is like "gemini-1.5-pro-latest"
    api_endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    url = f"{api_endpoint}?key={api_key}"

    payload = {
        "contents": [{"role": "user", "parts": [{"text": user_input_with_context}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {"temperature": 0.5, "maxOutputTokens": max_tokens},
    }

    logger.debug(f"Ask Tool: Payload generationConfig: {payload['generationConfig']}")

    try:
        response = requests.post(
            url, headers=headers, data=json.dumps(payload), timeout=API_TIMEOUT_SECONDS
        )
        logger.debug(f"Ask Tool: API Response Status: {response.status_code}")
        response.raise_for_status()
        response_data = response.json()

        if "candidates" in response_data and response_data["candidates"]:
            candidate = response_data["candidates"][0]
            finish_reason = candidate.get("finishReason", "UNKNOWN")
            logger.info(f"Ask Tool: API call finished with reason: {finish_reason}")

            if (
                "content" in candidate
                and "parts" in candidate["content"]
                and candidate["content"]["parts"]
            ):
                text_response = candidate["content"]["parts"][0]["text"]
                logger.info("Ask Tool: API call successful.")
                return text_response
            elif finish_reason != "STOP":
                if finish_reason == "SAFETY":
                    logger.error(
                        "Gemini API blocked the request due to safety concerns."
                    )
                    return "Error: Assistant response blocked due to safety concerns."
                elif finish_reason == "RECITATION":
                    logger.error(
                        "Gemini API blocked the request due to recitation concerns."
                    )
                    return (
                        "Error: Assistant response blocked due to recitation concerns."
                    )
                else:
                    logger.error(
                        f"API finished with reason '{finish_reason}' but no content.",
                        extra={"candidate": candidate},
                    )
                    return f"Error: Assistant finished with reason '{finish_reason}' but provided no content."
            else:
                logger.warning(
                    "API stopped but no content found.", extra={"candidate": candidate}
                )
                return "Error: Assistant stopped but provided no content."
        else:
            logger.warning(
                "No candidates found in API response.",
                extra={"response_data": response_data},
            )
            return "Error: No response candidates received from the assistant."

    except requests.exceptions.HTTPError as http_err:
        logger.error(
            f"HTTP error during Ask API call: {http_err}. URL: {api_endpoint}",
            exc_info=True,
        )
        error_body = "(Could not read error body)"
        if http_err.response is not None:
            try:
                error_body = http_err.response.text
            except Exception:
                pass
        return f"Error: Failed to get response from assistant (HTTP {http_err.response.status_code if http_err.response else 'N/A'}): {error_body[:500]}"
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception during Ask API call: {req_err}", exc_info=True)
        return f"Error: Failed to connect to assistant API: {req_err}"
    except Exception as e:
        logger.error(f"Unexpected error during Ask API call: {e}", exc_info=True)
        return f"Error: An unexpected error occurred: {e}"


# --- File Finding Logic & Tree Function ---
def find_files_by_extension(
    directories=None,
    extensions=DEFAULT_EXTENSIONS,
    exclude_dirs=DEFAULT_EXCLUDE_DIRS,
    exclude_files=DEFAULT_EXCLUDE_FILES,
):
    if directories is None:
        directories = ["."]

    extensions_with_dot = {
        ext if ext.startswith(".") else f".{ext}" for ext in extensions
    }
    exclude_dir_patterns = set(exclude_dirs)
    exclude_file_patterns = set(exclude_files)

    all_files = set()
    for directory in directories:
        base_dir = Path(directory).resolve()
        if not base_dir.is_dir():
            logger.warning(f"Directory '{directory}' does not exist, skipping...")
            continue

        for item in base_dir.rglob("*"):  # Recursive globbing
            # Check directory exclusion
            relative_parts = item.relative_to(base_dir).parts
            if any(
                fnmatch.fnmatch(part, pattern)
                for part in relative_parts
                for pattern in exclude_dir_patterns
            ):
                # Skip if any part of the path matches exclude_dirs
                # Also skip if the item itself matches (e.g., top-level '.git')
                if item.is_dir() and any(
                    fnmatch.fnmatch(item.name, pattern)
                    for pattern in exclude_dir_patterns
                ):
                    # Prevent descending into explicitly excluded top-level dirs like .git
                    pass  # Let the loop handle sub-items exclusion
                continue

            if item.is_file():
                # Check file extension
                if item.suffix.lower() in extensions_with_dot:
                    # Check file exclusion
                    if not any(
                        fnmatch.fnmatch(item.name, pattern)
                        for pattern in exclude_file_patterns
                    ):
                        # Check file size limit
                        try:
                            if item.stat().st_size <= MAX_FILE_SIZE_BYTES:
                                all_files.add(item)
                            else:
                                logger.debug(
                                    f"Skipping large file: {item} ({item.stat().st_size} bytes)"
                                )
                        except OSError as e:
                            logger.warning(
                                f"Could not stat file {item}: {e}. Skipping."
                            )

    return sorted(list(all_files))


def get_tree_output(exclude_dirs=DEFAULT_EXCLUDE_DIRS):
    try:
        exclude_flags = []
        for d in exclude_dirs:
            exclude_flags.extend(["-I", d])
        # Limit depth, show hidden, no report, use exclude flags
        command = ["tree", "-a", "-L", "3", "--noreport"] + exclude_flags
        logger.info(f"Running tree: {' '.join(command)}")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
            errors="ignore",
        )
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            if len(lines) > MAX_TREE_LINES:
                logger.warning(
                    f"Truncating tree output from {len(lines)} to {MAX_TREE_LINES} lines."
                )
                return (
                    "\n".join(lines[:MAX_TREE_LINES]) + "\n... (tree output truncated)"
                )
            return result.stdout
        else:
            logger.warning(
                f"'tree' command failed (Code: {result.returncode}). Stderr: {result.stderr}"
            )
            return "(tree command failed or not installed)"
    except FileNotFoundError:
        logger.warning("'tree' command not found. Install it for directory context.")
        return "(tree command not found)"
    except Exception as e:
        logger.error(
            f"An unexpected error occurred while running tree: {e}", exc_info=True
        )
        return "(Error running tree command)"


# --- File Reading and Context Creation ---
def read_file_content(file_path: Path) -> str | None:
    logger.debug(f"Reading file content: {file_path}")
    try:
        # Size check already done in find_files_by_extension
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}", exc_info=True)
        return None


def create_file_context(files: list[Path]) -> str:
    context = ""
    if not files:
        return context

    files_to_read = files[:MAX_FILES_FOR_CONTEXT]
    total_size = 0

    context_parts = ["\n\n--- Attached File Context ---"]
    read_count = 0
    for file_path in files_to_read:
        content = read_file_content(file_path)
        if content:
            try:
                relative_path = file_path.relative_to(Path.cwd())
            except ValueError:
                relative_path = file_path

            file_header = f"\n--- File: {relative_path} ---"
            file_content = f"\n{content}\n"
            current_part_size = len(file_header.encode("utf-8")) + len(
                file_content.encode("utf-8")
            )

            if total_size + current_part_size > MAX_CONTEXT_SIZE_BYTES:
                logger.warning(
                    f"Context size limit ({MAX_CONTEXT_SIZE_BYTES} bytes) reached. Skipping remaining files starting with {relative_path}."
                )
                context_parts.append("\n... (Context truncated due to size limit)")
                break

            context_parts.append(file_header)
            context_parts.append(file_content)
            total_size += current_part_size
            read_count += 1

    if len(files) > read_count:
        skipped_count = len(files) - read_count
        if len(files) > MAX_FILES_FOR_CONTEXT:
            limit_reason = f"{MAX_FILES_FOR_CONTEXT} file limit"
        else:
            limit_reason = f"{MAX_CONTEXT_SIZE_BYTES / 1024:.0f}KB size limit"
        context_parts.append(
            f"\n... (plus {skipped_count} more files not shown due to {limit_reason})"
        )

    context_parts.append("\n--- End Attached File Context ---")
    logger.info(
        f"Read content from {read_count} files for context ({total_size / 1024:.1f} KB)."
    )
    return "".join(context_parts)


# --- Tool Backend Function ---
def handle_ask(
    query: str, api_key: Optional[str] = None, model_name: Optional[str] = None
) -> str:
    """Handles the 'ask' tool request: gathers context and calls Gemini."""
    logger.info(f"--- Ask Tool (handle_ask): Received query: {query[:100]}... ---")
    base_dir = Path.cwd()

    # Check prerequisites passed from caller
    if not api_key:
        logger.error("Ask Tool: Missing API Key.")
        return "Error: Gemini API Key was not provided to handle_ask."
    if not model_name:
        logger.error("Ask Tool: Missing Model Name.")
        return "Error: Gemini model name was not provided to handle_ask."

    # 1. Get Project Tree
    logger.info("Ask Tool: Getting project tree structure...")
    tree_output = get_tree_output()

    # 2. Find Relevant Files
    logger.info("Ask Tool: Searching for relevant files...")
    relevant_files = find_files_by_extension(directories=[str(base_dir)])
    if relevant_files:
        logger.info(f"Ask Tool: Found {len(relevant_files)} potential context files.")
    else:
        logger.info("Ask Tool: No relevant files found for context.")

    # 3. Create File Context
    logger.info("Ask Tool: Creating context from file contents...")
    file_context = create_file_context(relevant_files)

    # 4. Construct Full Prompt for Gemini
    user_input_with_context = f"""
User Request:
{query}

--- Project Structure ---
{tree_output}
{file_context}
"""

    # 5. Call Gemini API
    logger.info("Ask Tool: Calling Gemini API...")
    response = call_gemini_for_ask(
        system_prompt=LEAD_ENGINEER_PROMPT,
        user_input_with_context=user_input_with_context,
        api_key=api_key,
        model_name=model_name,
        # max_tokens can be passed if needed, defaults to ASK_MAX_TOKENS
    )

    logger.info("--- Ask Tool: Finished processing query. ---")
    return response


# Keep main() for potential standalone testing if needed
def main():
    # This part is for standalone testing if you run `python -m assistant.tools.ask`
    # It expects JSON from stdin
    print("--- Running ask.py in standalone test mode ---", file=sys.stderr)
    try:
        # Example: echo '{"query": "Explain the main loop in cli.py"}' | python -m assistant.tools.ask
        input_json_str = sys.stdin.read()
        args = json.loads(input_json_str)
        query = args["query"]
        print(f"--- Query from stdin: {query} ---", file=sys.stderr)
        response = handle_ask(query)
        print("--- Response: ---", file=sys.stderr)
        print(response)  # Print response to stdout
    except Exception as e:
        print(f"Error in standalone main: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # Setup basic logging ONLY if run directly for testing
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    main()
