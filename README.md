# 🛡️ Cyber-Trace: Security Log Analysis Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Azure](https://img.shields.io/badge/Cloud-Azure-0078D4.svg)
![Databricks](https://img.shields.io/badge/Databricks-Auto_Loader-FF3621.svg)
![Status](https://img.shields.io/badge/Status-Refactored-success.svg)

## Project Overview
**Cyber-Trace** is a data engineering project designed to ingest, process, and analyze cybersecurity logs (focusing on **MITRE ATT&CK** scenarios).

The goal is to build a production-ready ETL pipeline using the **Medallion Architecture** (Bronze/Silver/Gold) capable of detecting anomalies and visualizing threat patterns from raw datasets (e.g., Mordor Project).

> **🔄 Migration Notice:** This project has been migrated from **AWS S3** to **Azure Data Lake Gen2 (ADLS)** to leverage Databricks native features like Auto Loader and Unity Catalog integration.

## Architecture & Tech Stack
* **Cloud Infrastructure:** Azure Data Lake Gen2 (Storage) + Azure Databricks (Compute).
* **Security:** Azure Key Vault + Databricks Secret Scopes.
* **ETL Engine:** Apache Spark (PySpark) Structured Streaming.
* **Ingestion Pattern:** Databricks **Auto Loader** (`cloudFiles`).
* **Data Format:** JSON (Raw) -> Delta Lake (Planned).

## Architectural Decisions Records (ADR)
Moving from a legacy prototype to a robust cloud architecture, several key decisions were made to ensure scalability and security:

### 1. Ingestion: Auto Loader vs. Standard Read
* **Decision:** Replaced standard `spark.read.json()` with Databricks **Auto Loader** (`cloudFiles`).
* **Context:** Standard directory listing in cloud storage (S3/ADLS) is slow and expensive for large datasets.
* **Benefit:** Auto Loader efficiently detects new files as they arrive, handles **Schema Evolution** automatically, and provides exactly-once processing guarantees via checkpointing.



### 2. Security: Key Vault vs. Local Config
* **Decision:** Migrated from local `project_config.py` files to **Azure Key Vault** backed by **Databricks Secret Scopes**.
* **Context:** Storing credentials in code or local files poses a security risk and complicates collaboration.
* **Benefit:** Credentials (SAS Tokens/Access Keys) are never exposed in the notebook. Access is managed via IAM roles and retrieved at runtime using `dbutils.secrets.get()`.

### 3. Fault Tolerance: Checkpointing
* **Decision:** Implemented explicit checkpointing for the streaming query.
* **Benefit:** Ensures the pipeline is resilient to cluster failures and restarts, resuming processing exactly where it left off without data duplication.

## Getting Started

### Prerequisites
* Azure Subscription with **ADLS Gen2** Storage Account.
* Azure **Key Vault** containing the storage access key.
* Databricks Workspace (Premium tier recommended for full security features).

### Installation & Setup
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/JakubMilczarczyk/Cyber-Trace.git](https://github.com/JakubMilczarczyk/Cyber-Trace.git)
    ```

2.  **Azure Setup:**
    * Create a container named `bronze` in your ADLS account.
    * Upload the raw Mordor logs (JSON) to a `raw_logs` folder.
    * Add your Storage Access Key to Azure Key Vault (Name: `storage-access-key`).

3.  **Databricks Configuration:**
    * Create a Secret Scope named `cybertrace-secrets` linked to your Key Vault.
    * Verify access in a notebook:
        ```python
        dbutils.secrets.list("cybertrace-secrets")
        ```

4.  **Run the Pipeline:**
    * Open `notebooks/01_ingest_bronze.ipynb`.
    * Run the initialization cell to configure authentication.
    * Run the streaming cell to start ingesting data.

## Roadmap
- [x] **Phase 1:** Ingestion (Bronze Layer) - Migrated to Azure & Auto Loader.
- [ ] **Phase 2:** Transformation (Silver Layer) - Data Cleaning & Schema Enforcement (Delta Lake).
- [ ] **Phase 3:** Aggregation (Gold Layer) - Business Logic & Threat Metrics.
- [ ] **Phase 4:** CI/CD & Unit Testing.

---
*Author: Jakub Milczarczyk*