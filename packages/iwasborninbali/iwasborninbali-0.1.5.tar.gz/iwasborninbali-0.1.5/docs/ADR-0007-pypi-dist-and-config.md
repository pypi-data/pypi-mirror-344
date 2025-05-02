# ADR-0007: PyPI Distribution and Configuration Loading Strategy

**Date:** 2024-05-17
**Status:** Accepted

## Context

The `platform-ai` CLI tool needs a standard distribution mechanism for users to install it easily. Additionally, it requires a flexible way to manage configuration, especially API keys, allowing users to set them globally, per project, or via environment variables.

## Decision

1.  **Distribution:** The package will be distributed via PyPI (`iwasborninbali`).
    *   Versioning will follow Semantic Versioning (SemVer).
    *   Builds will be handled using standard Python packaging tools (`build`).
    *   Uploads to PyPI will be managed using `twine`.
    *   Appropriate classifiers will be added to `pyproject.toml` to indicate target Python versions, license, OS compatibility, etc.

2.  **Configuration Loading:** Configuration values (like API keys) will be loaded using `python-dotenv` logic, searching the following locations. Values found in sources higher up the list take precedence (i.e., override values found lower down):
    1.  **OS Environment Variables:** System-level variables (e.g., set via `export`) have the highest priority.
    2.  **`PLATFORM_AI_CONFIG` Env Var:** Path specified by this variable pointing to a `.env` file.
    3.  **CWD `.env`:** A `.env` file in the current working directory.
    4.  **User Config `.env`:** A `.env` file at `~/.config/iwasborninbali/.env`.

## Consequences

*   **Pros:**
    *   Standard `pip install iwasborninbali` makes installation trivial.
    *   Clear versioning helps manage updates and compatibility.
    *   Layered configuration provides flexibility for different use cases (system-wide defaults, project-specific overrides, temporary overrides via env vars).
    *   Centralized configuration logic simplifies maintenance.
*   **Cons:**
    *   Requires maintaining PyPI package releases.
    *   Users need to understand the configuration precedence rules.

## Version History

*   **0.1.5 (2024-05-17):** Initial public release to PyPI (as `iwasborninbali`).
*   **Pre-release:** Versions prior to 0.1.5 were for internal development (as `platform-ai`). 