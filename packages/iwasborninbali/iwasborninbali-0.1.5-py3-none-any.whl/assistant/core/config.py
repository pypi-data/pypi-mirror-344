import os
import logging
from dotenv import load_dotenv
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def _load_env():
    """
    Load environment variables from .env file according to precedence:
    1. PLATFORM_AI_CONFIG environment variable (if set and file exists)
    2. .env file in the current working directory (CWD)
    3. .env file in ~/.config/platform-ai/
    OS environment variables always take precedence over values loaded from .env files.
    """
    config_path_var = os.getenv("PLATFORM_AI_CONFIG")
    cwd_path = Path.cwd() / ".env"
    home_config_path = Path.home() / ".config" / "platform-ai" / ".env"

    loaded_path = None

    # 1. Check PLATFORM_AI_CONFIG
    if config_path_var:
        explicit_path = Path(config_path_var)
        if explicit_path.is_file():
            logger.info(
                f"Loading environment variables from explicit path: {explicit_path}"
            )
            load_dotenv(dotenv_path=explicit_path, override=False)
            loaded_path = explicit_path
        else:
            logger.warning(
                f"PLATFORM_AI_CONFIG path specified but not found: {explicit_path}"
            )

    # 2. Check CWD .env (if not loaded via explicit path)
    if loaded_path is None and cwd_path.is_file():
        logger.info(f"Loading environment variables from CWD: {cwd_path}")
        load_dotenv(dotenv_path=cwd_path, override=False)
        loaded_path = cwd_path

    # 3. Check home directory .env (if not loaded previously)
    if loaded_path is None and home_config_path.is_file():
        # Ensure the directory exists before logging/loading (though is_file implies it)
        home_config_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(
            f"Loading environment variables from home config: {home_config_path}"
        )
        load_dotenv(dotenv_path=home_config_path, override=False)
        loaded_path = home_config_path

    if loaded_path is None:
        logger.info(
            "No .env file found in specified locations (PLATFORM_AI_CONFIG, CWD, ~/.config/platform-ai). Using system environment variables only."
        )


# Load environment variables at module import time
_load_env()

# --- API Keys ---
# It's recommended to set these via environment variables or a .env file
# Provide defaults or raise errors if critical keys are missing

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Check for critical missing keys (optional, depends on application needs)
# if not OPENAI_API_KEY:
#     logger.warning("OPENAI_API_KEY is not set. OpenAI features will be unavailable.")
# if not GEMINI_API_KEY:
#     logger.warning("GEMINI_API_KEY is not set. Google AI features will be unavailable.")
# if not PERPLEXITY_API_KEY:
#      logger.warning("PERPLEXITY_API_KEY is not set. Perplexity features will be unavailable.")


# --- Model Names ---
# Define the models to be used by different parts of the application.
# These can be overridden by setting the corresponding environment variables
# (e.g., MODEL_ASK, MODEL_REWRITE) or by placing them in a .env file.

# MODEL_MAIN: Reserved for potential future use or top-level control.
MODEL_MAIN = os.getenv("MODEL_MAIN", "o4-mini")

# MODEL_ASK: Used by the 'ask' tool for general queries, code understanding, and reviews.
# Requires high reasoning capability.
MODEL_ASK = os.getenv("MODEL_ASK", "gemini-2.5-pro-preview-03-25")

# MODEL_REWRITE: Used by file creation ('create_file') and modification ('apply_diff') tools.
# Needs to be efficient and good at following structured instructions.
MODEL_REWRITE = os.getenv("MODEL_REWRITE", "gemini-2.5-flash-preview-04-17")

# MODEL_PPLX: Used by the 'perplexity' tool for web searches and external information retrieval.
MODEL_PPLX = os.getenv("MODEL_PPLX", "sonar-reasoning-pro")

logger.info(
    f"Using models - Main: {MODEL_MAIN}, Ask: {MODEL_ASK}, Rewrite: {MODEL_REWRITE}, Perplexity: {MODEL_PPLX}"
)

# --- Other Configurations ---
# Example: Log level, file paths, etc.
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Update root logger level based on config
logging.getLogger().setLevel(LOG_LEVEL)


# Ensure the core directory exists if needed for imports elsewhere
if __name__ == "__main__":
    # Example usage or check
    print("Configuration loaded:")
    print(f"  OpenAI Key set: {'Yes' if OPENAI_API_KEY else 'No'}")
    print(f"  Gemini Key set: {'Yes' if GEMINI_API_KEY else 'No'}")
    print(f"  Perplexity Key set: {'Yes' if PERPLEXITY_API_KEY else 'No'}")
    print(f"  Main Model: {MODEL_MAIN}")
    print(f"  Ask Model: {MODEL_ASK}")
    print(f"  Rewrite Model: {MODEL_REWRITE}")
    print(f"  Perplexity Model: {MODEL_PPLX}")
    print(f"  Log Level: {LOG_LEVEL}")
