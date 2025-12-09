"""Tests for transformation functions."""

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from src.transformations import flatten_security_logs

@pytest.fixture(scope='session')
def spark():
    """Create a Spark session for testing."""
    return SparkSession.builder \
        .master('local[1]') \
        .appName('CyberTraceTest') \
        .getOrCreate()

def test_flatten_sysmon_log(spark):
    """Test flattening of a Sysmon log."""
    
    # Mock data
    data = [
        (
            "2020-09-20T06:57:17.371Z", 
            10, 
            "WORKSTATION5.theshire.local",
            "Microsoft-Windows-Sysmon/Operational",
            "C:\\windows\\system32\\svchost.exe"
        )
    ]

    # Flattened schema
    schema = StructType([
        StructField("@timestamp", StringType(), True),
        StructField("EventID", IntegerType(), True),
        StructField("Computer", StringType(), True),
        StructField("Channel", StringType(), True),
        StructField("CallTrace", StringType(), True)
    ])

    df_input = spark.createDataFrame(data, schema)

    df_result = flatten_security_logs(df_input)

    # assertions
    assert 'hostname' in df_result.columns
    assert "log_channel" in df_result.columns

    row = df_result.first()
    assert row["event_id"] == 10
    assert row["hostname"] == "WORKSTATION5.theshire.local"
    assert row["log_channel"] == "Microsoft-Windows-Sysmon/Operational"