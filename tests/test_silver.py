"""
Test cases for silver layer.
"""

import pytest
from src.transformations import standardize_security_logs
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType

def test_standardize_sysmon_event_10(spark):
    """
    Scenario: Sysmon Event 10 (Process Access) from Mordor Dataset.
    Goal: Verify if flat JSON fields are correctly mapped to Silver schema.
    """
    # 1. Arrange
    data = [{
        "@timestamp": "2020-09-20T06:57:17.371Z",
        "EventID": 10,
        "Hostname": "WORKSTATION5.theshire.local",
        "Channel": "Microsoft-Windows-Sysmon/Operational",
        "SourceImage": "C:\\windows\\system32\\svchost.exe",
        "TargetImage": "C:\\windows\\System32\\svchost.exe",
        "AccountName": "SYSTEM",
        "tags": ["mordorDataset"]
    }]

    df_raw = spark.createDataFrame(data)

    # 2. Act
    df_silver = standardize_security_logs(df_raw)

    # 3. Assert
    result = df_silver.collect()[0]

    assert result["event_id"] == 10
    assert result["hostname"] == "WORKSTATION5.theshire.local"
    assert result["process_image"] == "C:\\windows\\system32\\svchost.exe"
    assert result["user_account"] == "SYSTEM"
    assert result["event_timestamp"].year == 2020

def test_standardize_powershell_missing_fields(spark):
    """
    Scenario: PowerShell Event 4103.
    Goal: Verify that missing fields (e.g., SourceImage) result in Nulls, not Errors.
    """
    data = [{
        "@timestamp": "2020-09-20T06:57:17.372Z",
        "EventID": 4103,
        "Channel": "Microsoft-Windows-PowerShell/Operational",
        "ContextInfo": "Severity = Informational..."
        # No SourceImage in this record
    }]

    df_raw = spark.createDataFrame(data)
    df_silver = standardize_security_logs(df_raw)
    result = df_silver.collect()[0]

    assert result["event_id"] == 4103
    assert result["process_image"] is None  # SourceImage was missing
