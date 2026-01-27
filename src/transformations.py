"""Siver layer transformations.
Standarizes raw security logs into a schema optimized for Threat Hunting.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import TimestampType, IntegerType

def standarize_security_logs(df: DataFrame) -> DataFrame:
    """
    Standarizes schema for mixed security logs (Sysmon, PowerShell).
    Handles both flat and nested JSON structures via coalescing.

    Args:
        df (DataFrame): Raw Bronze DataFrame. 

    Returns:
        DataFrame: Standarized Silver DataFrame with 'event_timestamp' and 'host'.
    """

    timestamp_col = F.coalesce(
        F.col("@timestamp"),
        F.col("EventTime")
    ).cast(TimestampType())

    host_col = F.coalesce(
        F.col("Hostname"),
        F.col("host"),
        F.col("Computer")
    )

    def secure_col(col_name: str, nested_fallback: str = None): 
        if nested_fallback:
            return F.coalesce(F.col(col_name), F.col(nested_fallback))
        return F.col(col_name)

    df_silver = df.select(
        timestamp_col.alias("event_timestamp"),
        F.col("EventID").cast(IntegerType()).alias("event_id"),
        F.col("Channel").alias("log_channel"),
        host_col.alias("hostname"),

        # User Context
        F.coalesce(F.col("AccountName"), F.col("User"), F.col("UserID")).alias("user_account"),

        # Process / Execution Context
        secure_col("SourceImage", "EventData.SourceImage").alias("process_image"),
        secure_col("TargetImage", "EventData.TargetImage").alias("target_process_image"),
        secure_col("CommandLine", "EventData.CommandLine").alias("command_line"),

        # Network Context
        secure_col("SourceIp", "EventData.SourceIp").alias("source_ip"),
        secure_col("DestinationIp", "EventData.DestinationIp").alias("dest_ip"),
        secure_col("DestinationPort", "EventData.DestinationPort").alias("dest_port"),

        # Threat Context
        F.col("tags").alias("detection_tags")
    )

    # Data Quality Checks
    return df_silver.filter(F.col(event_timestamp).isNotNull())
