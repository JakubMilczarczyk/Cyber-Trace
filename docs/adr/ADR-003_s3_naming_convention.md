# ADR-003: S3 Folder Naming Standardization (Snake Case)

* **Status:** Accepted
* **Date:** 2025-11-18
* **Context:** Phase 1 (Infrastructure)

## Context and Problem
During the initial setup, S3 folders were created using human-readable names with spaces (e.g., `raw logs`).
This caused `PATH_NOT_FOUND` and URL parsing errors in the Spark/Hadoop S3A connector, which struggled to interpret spaces in the bucket path correctly.

## Decision
I enforced a strict **snake_case** naming convention for all S3 objects and folders.

* **Old Name:** `raw logs`
* **New Name:** `raw_logs`

## Consequences
* **Positive:** Ensures compatibility with Spark/Hadoop file system connectors. Improves predictability of file paths in scripts.
* **Negative:** None. This is a standard Data Engineering best practice.