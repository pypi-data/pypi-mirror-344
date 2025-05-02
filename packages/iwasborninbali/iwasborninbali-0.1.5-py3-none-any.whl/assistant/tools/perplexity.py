import json
import os
import requests
import sys
import logging
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any

logger = logging.getLogger(__name__)

# --- Configuration ---
MAX_ATTACHMENT_FILES = 10
MAX_ATTACHMENT_SIZE_BYTES = 200 * 1024
MAX_TOTAL_ATTACHMENT_SIZE = 1 * 1024 * 1024
API_TIMEOUT_SECONDS = 180
# --- End Configuration ---


# --- Attachment Handling Functions (keep as is) ---
def read_attachment_content(file_path: Path) -> Tuple[Optional[str], int]:
    """Читает контент файла аттачмента, проверяет размер."""
    logger.debug(f"Reading attachment file: {file_path}")
    try:
        if not file_path.is_file():
            logger.warning(f"Attachment file not found or is not a file: {file_path}")
            return f"Error: Attachment file not found: {file_path.name}", 0

        file_size = file_path.stat().st_size
        if file_size > MAX_ATTACHMENT_SIZE_BYTES:
            logger.warning(
                f"Skipping large attachment: {file_path.name} ({file_size} bytes > {MAX_ATTACHMENT_SIZE_BYTES})"
            )
            return (
                f"Error: Attachment file too large: {file_path.name} ({file_size} bytes)",
                0,
            )

        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
        logger.debug(f"Read {len(content)} chars from attachment {file_path.name}")
        return content, file_size
    except OSError as e:
        logger.error(f"OS error reading attachment {file_path}: {e}", exc_info=True)
        return f"Error reading attachment {file_path.name}: {e}", 0
    except Exception as e:
        logger.error(
            f"Unexpected error reading attachment {file_path}: {e}", exc_info=True
        )
        return f"Error reading attachment {file_path.name}: {e}", 0


def create_attachment_context(attachments: List[str], base_cwd: Path) -> str:
    """Создает строку контекста из указанных файлов аттачментов."""
    if not attachments:
        return ""

    logger.info(f"Processing {len(attachments)} attachments for Perplexity context...")
    context_parts = ["\n\n--- Attached Files Context ---"]
    files_processed = 0
    total_size = 0

    for file_rel_path in attachments[:MAX_ATTACHMENT_FILES]:
        if not isinstance(file_rel_path, str):
            logger.warning(
                f"Invalid attachment path type (expected string): {file_rel_path}. Skipping."
            )
            context_parts.append(f"\nError: Invalid attachment path: {file_rel_path}")
            continue

        file_path = (base_cwd / file_rel_path).resolve()
        content, file_size = read_attachment_content(file_path)

        try:
            relative_path_display = file_path.relative_to(base_cwd)
        except ValueError:
            relative_path_display = file_path  # Fallback if not relative

        file_header = f"\n--- File: {relative_path_display} ---"

        if content is None:
            content = "(Error reading file)"  # Use placeholder if read failed

        current_part_size = len(file_header.encode("utf-8", "ignore")) + len(
            content.encode("utf-8", "ignore")
        )  # Estimate size

        if total_size + current_part_size > MAX_TOTAL_ATTACHMENT_SIZE:
            logger.warning(
                f"Total attachment context size limit ({MAX_TOTAL_ATTACHMENT_SIZE} bytes) reached. Skipping remaining files starting with {relative_path_display}."
            )
            context_parts.append("\n... (Context truncated due to total size limit)")
            break

        context_parts.append(file_header)
        context_parts.append(f"\n{content}\n")
        total_size += current_part_size
        files_processed += 1

    if len(attachments) > files_processed:
        skipped_count = len(attachments) - files_processed
        limit_reason = (
            f"{MAX_ATTACHMENT_FILES} file limit"
            if files_processed == MAX_ATTACHMENT_FILES
            else f"{MAX_TOTAL_ATTACHMENT_SIZE / (1024 * 1024):.1f}MB total size limit"
        )
        context_parts.append(
            f"\n... (plus {skipped_count} more attachments not shown due to {limit_reason})"
        )

    context_parts.append("--- End Attached Files Context ---")
    logger.info(
        f"Processed {files_processed} attachments for Perplexity context ({total_size / 1024:.1f} KB)."
    )
    return "\n".join(context_parts)


# --- Main Tool Backend Function ---
def query_perplexity(
    query: str,
    project_root: Path,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None,  # Added model_name
    attachments: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Sends a query to the Perplexity AI API with optional attachments and returns the result.

    Args:
        query: The primary user query.
        project_root: The root directory of the project (for resolving attachment paths).
        api_key: Perplexity API key (from config).
        model_name: Perplexity model name (from config, e.g., MODEL_PPLX).
        attachments: Optional list of file paths relative to project_root.

    Returns:
        Dictionary with the API response or an error dictionary.
    """
    logger.debug(
        f"Handling query_perplexity. Query: '{query[:100]}...', Model: {model_name}, Attachments: {attachments}"
    )

    if not api_key:
        msg = "PERPLEXITY_API_KEY was not provided to query_perplexity tool."
        logger.error(msg)
        return {"error": {"message": msg, "type": "configuration_error"}}
    if not model_name:
        msg = "Perplexity model name was not provided to query_perplexity tool."
        logger.error(msg)
        return {"error": {"message": msg, "type": "configuration_error"}}

    # --- Create context from attachments ---
    attachment_context = (
        create_attachment_context(attachments, project_root) if attachments else ""
    )
    # Combine context and query
    final_query_content = (
        f"{attachment_context}\n\nUser Query: {query}" if attachment_context else query
    )
    # --- End context creation ---

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Perplexity API uses a specific system prompt format
    system_prompt = """You are a code research assistant that finds and presents relevant code snippets and best practices from across the web.

Your primary goals are:
1. Find ACTUAL CODE IMPLEMENTATIONS from:
   - Public GitHub repositories
   - Official documentation
   - Well-maintained open source projects
   - Recent blog posts and tutorials
2. Prioritize recent, well-maintained, and widely-used solutions
3. Include code snippets with proper attribution and context
4. Show multiple approaches when relevant
5. Highlight best practices and common pitfalls

FORMAT YOUR RESPONSES LIKE THIS:
For each code snippet:
```language
// Source: [repository/website name]
// URL: [source URL]
// Description: [brief context about this implementation]
[code snippet]
```

For best practices and patterns:
```markdown
- [practice 1]
- [practice 2]
...

- [pitfall 1]
- [pitfall 2]
...
```

ALWAYS include:
- Source attribution
- URLs to original content
- Brief context for each code snippet
- Version information if relevant
- Any important dependencies or requirements

Remember: Focus on providing ACTUAL, USABLE CODE with clear attribution and context."""

    payload = {
        "model": model_name,  # Use model from config
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": final_query_content},
        ],
        # Add other params like temperature, max_tokens if needed
    }

    logger.info(
        f"Sending request to Perplexity API ({model_name}). Total query length (incl. context): {len(final_query_content)} chars."
    )
    logger.debug(f"Payload for Perplexity: {json.dumps(payload)[:200]}...")

    try:
        response = requests.post(
            url, headers=headers, json=payload, timeout=API_TIMEOUT_SECONDS
        )
        logger.debug(f"Perplexity API response status: {response.status_code}")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        response_data = response.json()
        logger.debug(
            f"Perplexity API response JSON: {json.dumps(response_data)[:200]}..."
        )
        # Return the full JSON response as the tool result
        return response_data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Perplexity API request: {e}", exc_info=True)
        error_payload = {"error": {"message": str(e), "type": "request_error"}}
        if hasattr(e, "response") and e.response is not None:
            error_payload["error"]["status_code"] = e.response.status_code
            try:
                error_details = e.response.json()
                error_payload["error"]["details"] = error_details
                logger.error(f"Perplexity API error details: {error_details}")
            except Exception:
                error_details = e.response.text
                error_payload["error"]["details"] = error_details
                logger.error(f"Perplexity API error text: {error_details}")
        return error_payload
    except Exception as e:
        logger.error(
            f"Unexpected error during Perplexity API request: {e}", exc_info=True
        )
        return {"error": {"message": str(e), "type": "unexpected_error"}}


# Standalone testing function (optional)
if __name__ == "__main__":
    print("Testing perplexity standalone.")
    test_query = "Find python examples for reading a CSV file using pandas."
    # Create a dummy attachment file
    cwd = Path.cwd()
    test_attach_dir = cwd / "test_output"
    test_attach_dir.mkdir(exist_ok=True)
    test_attach_file = test_attach_dir / "perplexity_test.txt"
    test_attach_file.write_text("This is a test attachment file.", encoding="utf-8")
    test_attachments = [str(test_attach_file.relative_to(cwd))]

    # Load API key and model from environment (or config if available)
    try:
        from assistant.core import config  # Try importing config

        api_key = config.PERPLEXITY_API_KEY
        model = config.MODEL_PPLX
    except (ImportError, AttributeError):
        print("Could not import config, loading from environment variables.")
        api_key = os.getenv("PERPLEXITY_API_KEY")
        model = os.getenv(
            "MODEL_PPLX", "llama-3-sonar-large-32k-online"
        )  # Fallback default

    if not api_key:
        print(
            "Error: PERPLEXITY_API_KEY not found in config or environment.",
            file=sys.stderr,
        )
        sys.exit(1)
    if not model:
        print(
            "Error: Perplexity model name not found in config or environment.",
            file=sys.stderr,
        )
        sys.exit(1)

    result = query_perplexity(
        query=test_query,
        project_root=cwd,
        api_key=api_key,
        model_name=model,
        attachments=test_attachments,
    )

    print("--- Perplexity Response --- ")
    print(json.dumps(result, indent=2, ensure_ascii=False))
