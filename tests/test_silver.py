"""
Test cases for silver layer.
"""

import pytest
from src.transformations import standardize_security_logs

def test_standardize_ocsf_mapping_and_masking(spark):
    """
    Scenario: Validate OCSF Column Mapping and PII Masking.
    Goal: Check if 'SourceIp' becomes 'src_ip' AND is masked properly.
    """
    # 1. Arrange
    data = [{
        "@timestamp": "2020-09-20T06:57:17.371Z",
        "EventID": 10,
        "Hostname": "WORKSTATION5.theshire.local",
        "Channel": "Microsoft-Windows-Sysmon/Operational",
        "EventData": {
            "SourceIp": "192.168.1.50",       # To powinno zostać zamaskowane
            "DestinationIp": "10.0.0.1",      # To też
            "SourceImage": "C:\\windows\\system32\\svchost.exe",
            "DestinationPort": 443
        }
    }]
    
    df_raw = spark.createDataFrame(data)

    # 2. Act
    df_silver = standardize_security_logs(df_raw)

    # 3. Assert
    result = df_silver.collect()[0]
    
    # Test OCSF Naming Convention
    assert "src_ip" in df_silver.columns
    assert "process_path" in df_silver.columns
    
    # Test IP Masking Logic (Last octet should be XXX)
    assert result["src_ip"] == "192.168.1.XXX"
    assert result["dst_ip"] == "10.0.0.XXX"
    
    # Test Integer Casting
    assert result["dst_port"] == 443
    
    # Test Timestamp & Partition Key
    assert result["event_date"].isoformat() == "2020-09-20"

def test_missing_nested_fields_safety(spark):
    """
    Scenario: Input lacks 'EventData' completely.
    Goal: Pipeline should not crash, returning Nulls for mapped fields.
    """
    # 1. Arrange (Brak EventData)
    data = [{
        "@timestamp": "2020-09-20T08:00:00.000Z",
        "EventID": 4104,
        "Channel": "System"
    }]
    
    df_raw = spark.createDataFrame(data)

    # 2. Act
    df_silver = standardize_security_logs(df_raw)
    result = df_silver.collect()[0]

    # 3. Assert
    assert result["src_ip"] is None
    assert result["process_path"] is None
    assert result["event_id"] == 4104
