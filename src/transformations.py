"""Main transformations for silver layer data."""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, to_timestamp

def flatten_security_logs(df: DataFrame) -> DataFrame:
    """
    Standarize and flatten security logs (Mordor/Sysmon/Windows).
    Chose main columns to Lateral Movement analysys.

    Args:
        df (DataFrame): Raw security logs DataFrame.

    Returns:
        DataFrame: Flattened security logs DataFrame (Silver Layer).
    """
    if df.rdd.isEmpty():
        return df
    
    columns_to_select = []

    if '@timestamp' in df.columns:
        columns_to_select.append(col('@timestamp').cast('timestamp').alias('event_timestamp'))
    elif 'TimeCreated' in df.columns:
        columns_to_select.append(col('TimeCreated').cast('timestamp').alias('event_timestamp'))
    
    if 'EventID' in df.columns:
        columns_to_select.append(col('EventID').cast('integer').alias('event_id'))
    
    if 'Computer' in df.columns:
        columns_to_select.append(col('Computer').alias('hostname'))
    elif 'Hostname' in df.columns:
        columns_to_select.append(col('Hostname').alias('hostname'))

    if 'Channel' in df.columns:
        columns_to_select.append(col('Channel').alias('log_channel'))
    
    if 'EventData' in df.columns:
        # Source User / Account Name
        columns_to_select.append(col("EventData.User").alias("user_account"))
        columns_to_select.append(col("EventData.SourceUser").alias("source_user"))
        columns_to_select.append(col("EventData.TargetUserName").alias("target_user"))
        
        # Network
        columns_to_select.append(col("EventData.SourceIp").alias("source_ip"))
        columns_to_select.append(col("EventData.DestinationIp").alias("dest_ip"))
        columns_to_select.append(col("EventData.DestinationPort").alias("dest_port"))
        
        # Process
        columns_to_select.append(col("EventData.Image").alias("process_image"))
        columns_to_select.append(col("EventData.TargetImage").alias("target_process_image"))
        columns_to_select.append(col("EventData.CommandLine").alias("command_line"))
    
    if 'CallTrace' in df.columns:
        columns_to_select.append(col('CallTrace').alias('call_trace'))
    
    if 'AccountName' in df.columns:
        columns_to_select.append(col('AccountName').alias('account_name'))
    
    transformed_df = df.select(*columns_to_select)

    return transformed_df