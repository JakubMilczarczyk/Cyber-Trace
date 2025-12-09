# ADR-006: CI Strategy and Code Validation (Cost-Avoidance)

* **Status:** Accepted
* **Date:** 2025-12-09
* **Context:** Spinning up a Databricks cluster solely to detect syntax errors or logical bugs generates unnecessary cloud costs (Cluster startup time + DBU usage).
* **Decision:** Implementation of a Continuous Integration pipeline using GitHub Actions to validate code before cloud deployment:
  1. **Linter (Flake8):** For static code analysis and syntax error detection.
  2. [cite_start]**Unit Tests (PyTest):** For verifying transformation logic on a local Spark session (without Databricks runtime)[cite: 29].
  3. [cite_start]**Java Setup:** Configuration of the JVM environment (Temurin 11) within the CI runner to support PySpark execution[cite: 85].
* **Consequences:**
  * (+) Significant reduction in cloud costs (bugs are caught for free in GitHub Actions).
  * (+) Improved code quality and adherence to PEP8 standards.
  * (+) Prevention of merging broken code into the main branch (Quality Gate).