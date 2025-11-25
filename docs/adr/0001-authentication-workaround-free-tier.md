# ADR-001: Direct URI Injection for AWS S3 Authentication on Databricks Free Tier

* **Status:** Accepted
* **Date:** 2025-11-18
* **Context:** Phase 1 (Ingestion / Bronze Layer)

## Context and Problem
The project utilizes Databricks Community Edition (Free Tier) for compute and AWS S3 for storage.
The Free Tier environment enforces strict security isolation, preventing global modifications to the Spark configuration (`spark.conf.set` or `sc.hadoopConfiguration`).
Attempts to set `fs.s3a.access.key` globally result in a `[CONFIG_NOT_AVAILABLE]` error.
This limitation blocked the standard method of authenticating with AWS S3.

## Decision
I decided to use **Direct URI Credential Injection** to bypass the configuration restriction.
Instead of setting global configurations, AWS credentials are injected directly into the S3 URI path at runtime.

**Implementation Pattern:**
```python
s3_path = f"s3a://{ACCESS_KEY}:{SECRET_KEY}@{BUCKET_NAME}/{FILE_PATH}"
df = spark.read.json(s3_path)
```

## Consequences
* **Positive:** Enables data ingestion from AWS S3 within the constraints of the Databricks Free Tier without requiring a paid cluster.

* **Negative:** High security risk if the URI is printed or logged, as it exposes raw credentials.

* **Mitigation:** This decision necessitates the implementation of ADR-002 (Config Module Pattern) to ensure credentials are never hardcoded or visible in the codebase.