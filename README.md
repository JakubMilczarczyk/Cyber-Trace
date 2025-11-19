# Cyber-Trace: Security Log Analysis Pipeline 

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Databricks](https://img.shields.io/badge/Databricks-Free_Tier-orange.svg)
![AWS](https://img.shields.io/badge/AWS-S3-yellow.svg)
![Status](https://img.shields.io/badge/Status-In_Development-green.svg)

## Project Overview
**Cyber-Trace** is a data engineering project designed to ingest, process, and analyze cybersecurity logs (focusing on **MITRE ATT&CK** scenarios).

The goal is to build a production-ready ETL pipeline using the **Medallion Architecture** (Bronze/Silver/Gold) capable of detecting anomalies and visualizing threat patterns from raw datasets (e.g., Mordor Project).

## Architecture & Tech Stack
* **Cloud Infrastructure:** AWS S3 (Storage) + Databricks Community Edition (Compute).
* **ETL Engine:** Apache Spark (PySpark).
* **Data Format:** JSON (Raw Logs) -> Delta Lake (Planned).
* **Orchestration:** Databricks Notebooks (Prototype phase).

## Architectural Decisions & Constraints (ADR)
Since this project runs on a **Databricks Free Tier (Serverless Compute)** environment, several architectural adaptations were made to mimic production standards without incurring costs:

* **Authentication:** Due to the inability to set global Spark configurations (`spark.conf.set` is restricted in Free Tier), I implemented a **Direct URI Authentication** pattern using URL-encoded credentials injected securely at runtime.
* **Secrets Management:** Sensitive credentials are decoupled from the codebase using a local `project_config.py` module (Git-ignored) to maintain security best practices.
* **FinOps:** The architecture is designed to be strictly zero-cost during the prototyping phase (leveraging AWS Free Tier limits and Databricks Community Edition).

## Getting Started
### Prerequisites
* Python 3.10+
* Access to an AWS S3 Bucket
* Databricks Community Edition Account

### Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Cyber-Trace.git](https://github.com/YOUR_USERNAME/Cyber-Trace.git)
    ```
2.  Install dependencies (for local testing):
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configuration:** Create a `project_config.py` file in the root directory (do NOT commit this):
    ```python
    settings = {
        "AWS_ACCESS_KEY": "YOUR_KEY",
        "AWS_SECRET_KEY": "YOUR_SECRET",
        "S3_BUCKET": "your-bucket-name",
        "S3_FOLDER": "raw_logs",
        "S3_FILE_NAME": "target_file.json"
    }
    ```

## Roadmap
- [x] **Phase 1:** Ingestion (Bronze Layer) - AWS S3 Connection & Raw Read.
- [ ] **Phase 2:** Transformation (Silver Layer) - Schema Parsing & Data Cleaning.
- [ ] **Phase 3:** Aggregation (Gold Layer) - Business Logic & Threat Metrics.
- [ ] **Phase 4:** CI/CD & Unit Testing.

---
*Author: Jakub Milczarczyk*