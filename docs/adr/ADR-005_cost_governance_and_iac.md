# ADR-005: FinOps Strategy and Rejection of IaC (Terraform)

* **Status:** Accepted
* **Date:** 2025-12-09
* **Context:** The project is entering the migration phase to a paid AWS/Databricks infrastructure. There is a significant risk of uncontrolled costs and the potential trap of "overengineering" the infrastructure setup for a single-person project.
* **Decision:**
  1. [cite_start]**AWS Budgets:** Implementation of a strict budget cap (10 USD/month) using the "Simplified Template" with e-mail alerts triggered at 85% of the forecasted spend[cite: 20].
  2. **No IaC (Terraform):** Conscious decision to reject Terraform/CloudFormation at this stage. Infrastructure components (S3, IAM, Clusters) will be configured manually ("ClickOps") or via simple CLI scripts to adhere to the KISS principle.
  3. [cite_start]**Cluster Policy:** Enforcement of "Spot Instances" and "Single Node" cluster mode for all development workloads to minimize compute costs[cite: 66, 134].
* **Consequences:**
  * (+) Drastic simplification of the technology stack (no need to manage remote .tfstate).
  * (+) Faster delivery of business value (focus on PySpark logic, not HCL syntax).
  * (+) Financial safety guaranteed by the AWS Budgets layer, independent of code deployment.
  * (-) Harder to replicate the environment in the future (acceptable trade-off for an educational project).