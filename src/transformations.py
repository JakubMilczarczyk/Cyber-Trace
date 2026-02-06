"""
Silver layer transformations.
Standarizes raw security logs into a schema optimized for Threat Hunting.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import TimestampType, IntegerType

def standardize_security_logs(df: DataFrame) -> DataFrame:
    """
    Standardizes schema for mixed security logs (Sysmon, PowerShell).
    Handles both flat and nested JSON structures via coalescing.

    Args:
        df (DataFrame): Raw Bronze DataFrame. 

    Returns:
        DataFrame: Standardized Silver DataFrame.
    """
    # Helper Function: Safe Column Select
    def safe_col(col_name: str):
        if col_name in df.columns:
            return F.col(col_name)
        return F.lit(None)

    # Timestamp Standardization
    timestamp_col = F.coalesce(
        safe_col("@timestamp"),
        safe_col("EventTime")
    ).cast(TimestampType())

    # Hostname Standardization
    host_col = F.coalesce(
        safe_col("Hostname"),
        safe_col("host"),
        safe_col("Computer")
    )

    # User Standardization
    user_col = F.coalesce(
        safe_col("AccountName"),
        safe_col("User"),
        safe_col("UserID")
    )

    # Nested Fields Handling
    def secure_nested(flat_name, nested_name):
        cols_to_check = []

        if flat_name in df.columns:
            cols_to_check.append(F.col(flat_name))
        
        # Check for nested structure defensively
        try:
            cols_to_check.append(F.col(nested_name))
        except:
            pass

        if not cols_to_check:
            return F.lit(None).cast("string")
        
        return F.coalesce(*cols_to_check)
    
    # Define Transformations
    df_silver = df.select(
        timestamp_col.alias("event_timestamp"),
        safe_col("EventID").cast(IntegerType()).alias("event_id"),
        safe_col("Channel").alias("log_channel"),
        host_col.alias("hostname"),
        user_col.alias("user_account"),

        # Process / Execution Context
        secure_nested("SourceImage", "EventData.SourceImage").alias("process_image"),
        secure_nested("TargetImage", "EventData.TargetImage").alias("target_process_image"),
        secure_nested("CommandLine", "EventData.CommandLine").alias("command_line"),

        # Network Context
        secure_nested("SourceIp", "EventData.SourceIp").alias("source_ip"),
        secure_nested("DestinationIp", "EventData.DestinationIp").alias("dest_ip"),
        secure_nested("DestinationPort", "EventData.DestinationPort").alias("dest_port"),

        # Threat Context
        safe_col("tags").alias("detection_tags")
    )

    # Data Quality Checks
    return df_silver.filter(F.col("event_timestamp").isNotNull())

