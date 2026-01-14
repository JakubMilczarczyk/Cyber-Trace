# ADR-007: Migration to Azure Ecosystem & Auto Loader Implementation

* **Status:** Accepted
* **Date:** 2026-01-14
* **Context:** The initial AWS S3 + Databricks Community Edition setup imposed severe limitations on security configuration (inability to set global Spark configs) and performance (listing large directories in S3). To proceed with a production-grade Silver Layer, robust authentication and ingestion mechanisms were required.
* **Decision:** Migration of the entire infrastructure to the **Microsoft Azure** ecosystem:
  1. **Storage:** Azure Data Lake Gen2 (ADLS) replaces AWS S3.
  2. **Security:** Azure Key Vault + Databricks Secret Scopes replace direct URI injection.
  3. **Ingestion:** Databricks Auto Loader (`cloudFiles`) replaces standard `spark.read.json`.
* **Consequences:**
  * (+) **Security:** Zero-trust approach implemented; credentials are never exposed in the runtime.
  * (+) **Scalability:** Auto Loader eliminates file listing bottlenecks, allowing for efficient incremental processing.
  * (+) **Resilience:** Native checkpointing support ensures fault tolerance.
  * (-) **Cost:** Transition from Free Tier to Pay-As-You-Go model (requires FinOps monitoring).