# ADR 011: V2 Table Migration Strategy

## Status
Accepted

## Context
During the implementation of Time-Series Partitioning, we encountered a Schema Mismatch error. Delta Lake does not allow changing partitioning strategies on existing tables via simple `writeStream`. The legacy environment prevented physical deletion (`DROP TABLE`) of old managed tables.

## Decision
We adopted a **Blue-Green Migration approach (V2)** by creating new table entities (`*_v2`) and new checkpoint locations.

## Consequences
* **Positive:** Allowed seamless deployment of partitioning without downtime or complex manual cleanup.
* **Negative:** Left orphaned "v1" tables in the metastore (to be cleaned up by admin scripts later).