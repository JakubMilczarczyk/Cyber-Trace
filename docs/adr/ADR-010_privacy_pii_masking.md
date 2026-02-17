# ADR 010: Hard-Masking of PII for GDPR Compliance

## Status
Accepted

## Context
The dataset contains raw IP addresses. To comply with GDPR and internal security policies ("Privacy by Design"), analysts should not have access to full PII (Personally Identifiable Information) unless authorized. Current infrastructure (Legacy Hive Metastore) does not support dynamic row-level security.

## Decision
We implemented **ETL-level Hard Masking** in the Silver layer using PySpark regex transformations.
Logic: `mask_ip(ip)` replaces the last octet with `XXX` (e.g., `192.168.1.50` -> `192.168.1.XXX`).

## Consequences
* **Positive:** Guaranteed privacy compliance; data cannot be leaked accidentally from Gold/Silver tables.
* **Negative:** Security Operators cannot trace specific hosts in the analytical layer (requires raw logs access for deep dive).