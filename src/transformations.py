"""
Silver layer transformations.
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
        DataFrame: Standarized Silver DataFrame.
    """
    # Helper Function: Safe Column Select
    def safe_col(col_name: str):
        if col_name in df.columns:
            return F.col(col_name)
        return F.lit(None)

    # Timestamp Standarization
    timestamp_col = F.coalesce(
        safe_col("@timestamp"),
        safe_col("EventTime")
    ).cast(TimestampType())

    # Hostname Standarization
    host_col = F.coalesce(
        safe_col("Hostname"),
        safe_col("host"),
        safe_col("Computer")
    )

    # User Standarization
    user_col = F.coalesce(
        safe_col("AccountName"),
        safe_col("User"),
        safe_col("UserID")
    )

    # Nasted Fields Handling
    def secure_nasted(flat_name, nasted_name):
        cols_to_check = []

        if flat_name in df.columns:
            cols_to_check.append(F.col(flat_name))

        if "EventData" in df.columns:
            cols_to_check.append(F.col(nasted_name))

        if not cols_to_check:
            return F.lit(None).cast("string")
        
        return F.coalesce(*cols_to_check)
    
    # Define Transformations
    df_silver = df.select(
        timestamp_col.alias("event_timestamp"),
    
        # Event ID
        safe_col("EventID").cast(IntegerType()).alias("event_id"),

        safe_col("Channel").alias("log_channel"),
        host_col.alias("hostname"),
        user_col.alias("user_account"),

        # Process / Ececution Context
        secure_nasted("SourceImage", "EventData.SourceImage").alias("process_image"),
        secure_nasted("TargetImage", "EventData.TargetImage").alias("target_process_image"),
        secure_nasted("CommandLine", "EventData.CommandLine").alias("command_line"),

        # Network Context
        secure_nasted("SourceIp", "EventData.SourceIp").alias("source_ip"),
        secure_nasted("DestinationIp", "EventData.DestinationIp").alias("dest_ip"),
        secure_nasted("DestinationPort", "EventData.DestinationPort").alias("dest_port"),

        # Threat Context
        safe_col("tags").alias("detetion_tags")
    )

    # Data Quality Checks
    return df_silver.filter(F.col("event_timestamp").isNotNull())

    # def secure_col(col_name: str, nested_fallback: str = None): 
    #     if nested_fallback:
    #         return F.coalesce(F.col(col_name), F.col(nested_fallback))
    #     return F.col(col_name)

    # df_silver = df.select(
    #     timestamp_col.alias("event_timestamp"),
    #     F.col("EventID").cast(IntegerType()).alias("event_id"),
    #     F.col("Channel").alias("log_channel"),
    #     host_col.alias("hostname"),

    #     # User Context
    #     F.coalesce(F.col("AccountName"), F.col("User"), F.col("UserID")).alias("user_account"),

    #     # Process / Execution Context
    #     secure_col("SourceImage", "EventData.SourceImage").alias("process_image"),
    #     secure_col("TargetImage", "EventData.TargetImage").alias("target_process_image"),
    #     secure_col("CommandLine", "EventData.CommandLine").alias("command_line"),

    #     # Network Context
    #     secure_col("SourceIp", "EventData.SourceIp").alias("source_ip"),
    #     secure_col("DestinationIp", "EventData.DestinationIp").alias("dest_ip"),
    #     secure_col("DestinationPort", "EventData.DestinationPort").alias("dest_port"),

    #     # Threat Context
    #     F.col("tags").alias("detection_tags")
    # )

    # # Data Quality Checks
    # return df_silver.filter(F.col(event_timestamp).isNotNull())
