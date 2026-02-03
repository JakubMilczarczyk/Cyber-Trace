# ADR-009: FinOps Strategy for Streaming Execution

**Status:** Accepted
**Date:** 2026-02-03
**Context:**
The project utilizes Spark Structured Streaming. The default "Continuous Processing" mode requires the Spark cluster to run 24/7, generating high infrastructure costs on Azure Databricks that are unjustified for the current data volume and SLA requirements (no sub-second real-time requirement).

**Decision:**
We adopted the **`Trigger.AvailableNow`** (Micro-batch execution) mode for the Silver Layer write operations.

**Consequences:**
* **Positive:** Drastic **Cost Avoidance**. The cluster starts, processes all available data in a single batch, and shuts down.
* **Positive:** Maintains streaming semantics (checkpoints, exactly-once guarantees), allowing a seamless switch to continuous mode in the future if SLAs change.
* **Negative:** Increases data latency; Silver data is only available after the scheduled job execution (e.g., hourly), not in near real-time.