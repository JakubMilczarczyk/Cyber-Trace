# ADR-002: Config Module Pattern for Secret Management

* **Status:** Accepted
* **Date:** 2025-11-18
* **Context:** Phase 1 (Security & Best Practices)

## Context and Problem
Following the decision to use Direct URI Injection (ADR-001), the handling of AWS credentials became a critical security concern.
Hardcoding secrets (Access Keys/Secret Keys) directly in Databricks Notebooks poses a severe risk of accidental exposure when pushing code to public repositories (GitHub).
Databricks Secrets (Key Vault) is not available in the Community Edition.

## Decision
I adopted the **Config Module Pattern** to decouple secrets from the application logic.

1.  **Separation:** Secrets are stored in a local Python module named `project_config.py`.
2.  **Exclusion:** The `project_config.py` file is added to `.gitignore`.
3.  **Usage:** The main notebook imports this module to access credentials dynamically.

**Code Structure:**
```python
# project_config.py (Local only)
access_key = "AKI..."
secret_key = "SECRET..."
```

# Notebook
import project_config as cfg

# Usage
mount_point = f"s3a://{cfg.access_key}..."

# Consequences
* **Positive:** Eliminates the risk of leaking credentials to GitHub. Adheres to "Clean Code" principles.

* **Negative:** Requires manual setup of the config file when moving to a new environment (e.g., CI/CD or a new developer machine).