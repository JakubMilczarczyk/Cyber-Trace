# ADR-008: Defensive Transformation Logic for Silver Layer

**Status:** Accepted
**Date:** 2026-02-03
**Context:**
Raw security logs in the Bronze Layer originate from heterogeneous sources (Sysmon, PowerShell, Windows Event Logs). The JSON structure is volatile; fields like `Hostname`, `Computer`, or `SourceImage` appear interchangeably or are nested within `EventData`. Standard SQL schema enforcement leads to `AnalysisException` and pipeline failures when expected columns are missing.

**Decision:**
We decided to implement a **Defensive Programming** pattern in the transformation layer (PySpark API) by:
1.  Dynamically checking for column existence (`if col in df.columns`).
2.  Using `coalesce` to map multiple potential field names to a single standardized column (e.g., `Hostname` + `Computer` -> `hostname`).
3.  Abstracting this logic into a testable `standardize_security_logs` function in `src.transformations`.

**Consequences:**
* **Positive:** The pipeline is resilient to **Schema Drift**. Missing columns are safely filled with `NULL` instead of causing a critical crash.
* **Positive:** Logic is decoupled from the Notebook, enabling effective Unit Testing via `pytest`.
* **Negative:** Slightly higher computational complexity compared to a rigid SQL selection, but acceptable given the stability requirements.