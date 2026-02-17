"""
Silver layer transformations.
Standarizes raw security logs into a schema aligned with OCSF principles (Flat Version).
Includes PII masking and Time-Series preparation.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import TimestampType, IntegerType

def standardize_security_logs(df: DataFrame) -> DataFrame:
    """
    Standardizes schema for mixed security logs.
    Applies Privacy Masking (GDPR) and prepares Partition Key.

    Args:
        df (DataFrame): Raw Bronze DataFrame. 

    Returns:
        DataFrame: Standardized Silver DataFrame with masked IPs.
    """
    df_columns = df.columns

    # Helper Function: Safe Column Select
    def safe_col(col_name: str):
        if col_name in df_columns:
            return F.col(col_name)
        return F.lit(None)

    # Nested Fields Handling
    def secure_nested(flat_name, nested_parent, nested_field):
        cols_to_check = []

        if flat_name in df_columns:
            cols_to_check.append(F.col(flat_name))
        
        # Check for nested structure defensively
        if nested_parent in df_columns:
            cols_to_check.append(F.col(f"{nested_parent}.{nested_field}"))

        if not cols_to_check:
            return F.lit(None).cast("string")
        
        return F.coalesce(*cols_to_check)
    
    # Business Logic: IP Masking (Privacy)
    def mask_ip(col_expr):
        return F.regexp_replace(col_expr, r"(\d{1,3})$", "XXX")

    # --- TRANSFORMATIONS ---

    # Timestamp & Partition Key
    timestamp_col = F.coalesce(safe_col("@timestamp"), safe_col("EventTime")).cast(TimestampType())

    df_silver = df.select(
        timestamp_col.alias("event_timestamp"),
        F.to_date(timestamp_col).alias("event_date"),
    
        # Event Context
        safe_col("EventID").cast(IntegerType().alias("event_id")),
        safe_col("Channel").alias("log_channel"),

        # Actor Context
        safe_col("Hostname").alias("hostname"),         # OCSF: device.hostname
        safe_col("AccountName").alias("user_account"),  # OCSF: actor.user.name

        # Process Context
        secure_nested("SourceImage", "EventData", "SourceImage").alias("process_path"),
        secure_nested("TargetImage", "EventData", "TargetImage").alias("target_process_path"),
        secure_nested("CommandLine", "EventData", "CommandLine").alias("command_line"),

        # Network Context (Standardized & Masked)
        # OCSF Mapping: src_endpoint.ip, dst_endpoint.ip
        mask_ip(secure_nested("SourceIp", "EventData", "SourceIp")).alias("src_ip"),
        mask_ip(secure_nested("DestinationIp", "EventData", "DestinationIp")).alias("dst_ip"),

        secure_nested("DestinationPort", "EventData", "DestinationPort").cast(IntegerType()).alias("dst_port"),

        # Detection Context
        safe_col("tags").alias("detection_tags")
    )

    # Data Quality Filter
    return df_silver.filter(F.col("event_timestamp").isNotNull())
