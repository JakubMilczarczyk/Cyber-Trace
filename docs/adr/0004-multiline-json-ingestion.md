# ADR-004: Handling Multiline JSON for Security Logs

* **Status:** Accepted
* **Date:** 2025-11-18
* **Context:** Phase 1 (Ingestion)

## Context and Problem
The source data (OTRF/Mordor dataset) consists of security logs exported as nested JSON objects.
The standard `spark.read.json()` command expects one JSON object per line (JSONL). However, the source files are formatted as a standard JSON list or span multiple lines, causing the default reader to fail or corrupt the schema.

## Decision
I explicitly enabled the `multiline` option in the Spark reader.

**Implementation:**
```python
df = spark.read.option("multiline", "true").json(path)
```

# Consequences
* **Positive:** Correctly parses nested structures (like EventData and System fields) into a Spark DataFrame.

* **Negative:** The multiline option forces Spark to read the entire file on a single executor (cannot be split in parallel during the read phase), which may impact performance for extremely large files (Terabytes).

* **Mitigation:** For this project scale (GBs), the performance impact is negligible. For production at scale, an upstream process should convert files to JSONL or Parquet.