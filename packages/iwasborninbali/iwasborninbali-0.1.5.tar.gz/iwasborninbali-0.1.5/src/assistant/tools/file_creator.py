import os
import sys
import json
import requests
import logging
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

# Constants (can be adjusted)
API_TIMEOUT_SECONDS = 120
MAX_OUTPUT_TOKENS_REWRITE = 8192


# --- Helper function to clean Gemini response ---
def clean_gemini_response(content: str) -> str:
    """Removes markdown code fences if they wrap the entire response."""
    if content and content.startswith("```") and content.endswith("```"):
        lines = content.splitlines()
        if len(lines) > 1:
            # Check if the first line after ``` is just a language tag
            first_line_content = lines[0][3:].strip()
            if (
                first_line_content
                and " " not in first_line_content
                and len(first_line_content) < 15
            ):  # Heuristic for language tag
                cleaned = "\n".join(lines[1:-1])
            else:
                # Assume ``` was part of the intended content, remove only trailing ```
                cleaned = "\n".join(lines[:-1])
                if cleaned.startswith("```"):
                    cleaned = cleaned[3:]  # Remove leading ``` if it remained

            if cleaned.strip():  # Return cleaned content only if it's not empty
                logger.debug(
                    "Removed Markdown code fences from Gemini rewrite response."
                )
                return cleaned
    # If no fences or cleaning resulted in empty string, return original
    return content


# --- Gemini API Call for Content Rewrite ---
def call_gemini_for_content_rewrite(
    content_to_rewrite: str, api_key: str, model_name: str
) -> str | None:
    """Calls the specified Gemini model to clean/rewrite content for a new file."""
    logger.debug(f"Calling Gemini model '{model_name}' for content rewrite.")
    if not api_key:
        logger.error("GEMINI_API_KEY was not provided for content rewrite.")
        return None  # Indicate failure clearly
    if not model_name:
        logger.error("Gemini model name was not provided for content rewrite.")
        return None

    rewrite_system_prompt = (
        "You are an expert code editor/formatter. You will receive text content intended for a new file. "
        "Your task is to review this content, correct any potential JSON escaping issues or markdown artifacts, "
        "ensure it's well-formatted, and return ONLY the final, clean content suitable for direct saving to a file. "
        "Do not add any explanations, comments, or markdown code fences around the final content."
    )
    # Combine system prompt and user content into the user role for simpler models
    combined_user_prompt = f"{rewrite_system_prompt}\n\nPlease review and clean the following content for a new file:\n\n```\n{content_to_rewrite}\n```"

    headers = {"Content-Type": "application/json"}
    api_endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    gemini_url = f"{api_endpoint}?key={api_key}"

    request_data = {
        "contents": [{"role": "user", "parts": [{"text": combined_user_prompt}]}],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": MAX_OUTPUT_TOKENS_REWRITE,
        },
        # No systemInstruction for older Gemini API structure, included in user prompt
    }

    logger.info(f"Sending content rewrite request to Gemini model {model_name}...")
    try:
        response = requests.post(
            gemini_url, headers=headers, json=request_data, timeout=API_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        data = response.json()
        logger.debug(f"Gemini Response (rewrite): {json.dumps(data)[:200]}...")

        if "candidates" in data and data["candidates"]:
            candidate = data["candidates"][0]
            finish_reason = candidate.get("finishReason", "UNKNOWN")
            logger.info(f"Gemini rewrite finished with reason: {finish_reason}")

            if (
                "content" in candidate
                and "parts" in candidate["content"]
                and candidate["content"]["parts"]
            ):
                rewritten_content = candidate["content"]["parts"][0]["text"].strip()
                if rewritten_content:
                    logger.info("Content successfully rewritten by Gemini.")
                    # Clean potential wrapping fences added by the model
                    return clean_gemini_response(rewritten_content)
                else:
                    logger.warning("Gemini rewrite response was empty.")
                    return content_to_rewrite  # Return original if rewrite is empty
            elif finish_reason != "STOP":
                logger.error(
                    f"Gemini rewrite API finished with reason '{finish_reason}' but no content.",
                    extra={"response_data": data},
                )
                return None  # Indicate failure
            else:  # STOP but no content
                logger.warning(
                    "Gemini rewrite API stopped but no content found.",
                    extra={"response_data": data},
                )
                return None  # Indicate failure
        else:  # No candidates
            logger.warning(
                "No candidates found in Gemini rewrite response.",
                extra={"response_data": data},
            )
            return None  # Indicate failure

    except requests.exceptions.HTTPError as e:
        logger.error(
            f"HTTP error calling Gemini rewrite ({model_name}): {e}", exc_info=True
        )
        if e.response is not None:
            logger.error(f"Response text: {e.response.text}")
        return None  # Indicate failure
    except Exception as e:
        logger.error(
            f"Unexpected error calling Gemini rewrite ({model_name}): {e}",
            exc_info=True,
        )
        return None  # Indicate failure


# --- Main Tool Backend Function ---
def handle_create_file(
    target_file: str,
    content: str,
    project_root: Path,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None,
) -> Tuple[bool, str]:
    """
    Handles the create_file tool request.
    Rewrites content using Gemini and saves the file relative to project_root.

    Args:
        target_file: Relative path from project_root for the file.
        content: Initial content provided by the LLM.
        project_root: The root directory of the project (usually CWD).
        api_key: Gemini API key.
        model_name: Gemini model name for rewriting (e.g., MODEL_REWRITE).

    Returns:
        Tuple (success: bool, message: str)
    """
    # --- Initial Validation ---
    if not target_file or content is None:
        msg = f"Error: Invalid arguments for create_file. Missing 'target_file' or 'content'. Target: '{target_file}', Content Provided: {content is not None}"
        logger.error(msg)
        return False, msg
    # --- End Initial Validation ---

    logger.debug(
        f"Handling create_file. Target: '{target_file}', Project Root: '{project_root}', Content Length: {len(content)}"
    )

    if not api_key or not model_name:
        logger.warning(
            f"API Key or Model Name missing for rewrite in create_file ('{target_file}'). Saving raw content."
        )
        final_content = content  # Skip rewrite if config missing
    else:
        logger.info(
            f"Sending content for file '{target_file}' ({len(content)} bytes) to Gemini ({model_name}) for rewrite..."
        )
        final_content = call_gemini_for_content_rewrite(content, api_key, model_name)

        if final_content is None:
            # Rewrite failed, do not proceed with file creation
            error_msg = f"Error: Failed to rewrite content for file '{target_file}' using Gemini. File not created/modified."
            logger.error(error_msg)
            return False, error_msg

    # Determine the full path relative to the project root
    target_path = Path(target_file)
    if target_path.is_absolute():
        # Try to make it relative to project_root if it's inside
        try:
            relative_path = target_path.relative_to(project_root)
            full_path = project_root / relative_path
            logger.warning(
                f"Absolute path '{target_path}' provided; interpreted as '{full_path}' relative to project root '{project_root}'."
            )
        except ValueError:
            # If it's absolute but outside the project root, this is likely an error/security risk
            error_msg = f"Error: Absolute path '{target_path}' is outside the project root '{project_root}'. File creation disallowed."
            logger.error(error_msg)
            return False, error_msg
    else:
        # Relative path is expected
        full_path = project_root / target_file

    # Normalize the path (e.g., removes ../)
    full_path = full_path.resolve()

    # Security check: Ensure the resolved path is still within the project root
    if project_root not in full_path.parents and full_path != project_root:
        # This catches cases like `../../outside_file` after resolution
        error_msg = f"Error: Resolved path '{full_path}' is outside the project root '{project_root}'. File creation disallowed."
        logger.error(error_msg)
        return False, error_msg

    logger.info(f"Attempting to write file to resolved path: {full_path}")

    # Create parent directories if they don't exist
    dir_path = full_path.parent
    if dir_path:
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {dir_path}")
        except Exception as e:
            error_msg = (
                f"Error creating directories '{dir_path}' for file '{target_file}': {e}"
            )
            logger.error(error_msg, exc_info=True)
            return False, error_msg

    # Write the file
    try:
        file_exists = full_path.exists()
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(final_content)

        action = "overwritten" if file_exists else "created"
        final_output = (
            f"File '{target_file}' successfully {action}. (Path: {full_path})"
        )
        logger.info(final_output)
        return True, final_output
    except Exception as e:
        error_msg = f"Error writing file '{target_file}' to path '{full_path}': {e}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg


# Keep main for potential standalone testing
if __name__ == "__main__":
    # Example usage for testing - requires environment variables
    print("Testing file_creator standalone.")
    test_content = 'def hello():\n  print("Hello World!")\nhello()'
    test_target = "test_output/created_file.py"
    test_api_key = os.getenv("GEMINI_API_KEY")
    test_model = os.getenv(
        "MODEL_REWRITE", "gemini-1.5-flash-latest"
    )  # Get from env or use default
    cwd = Path.cwd()

    if not test_api_key:
        print(
            "Error: GEMINI_API_KEY environment variable not set for testing.",
            file=sys.stderr,
        )
        sys.exit(1)

    success, message = handle_create_file(
        target_file=test_target,
        content=test_content,
        project_root=cwd,
        api_key=test_api_key,
        model_name=test_model,
    )
    print(f"Success: {success}")
    print(f"Message: {message}")
