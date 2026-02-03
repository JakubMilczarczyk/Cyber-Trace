"""Configuration environment for tests"""

import pytest
import sys
import os
from pyspark.sql import SparkSession

@pytest.fixture(scope='session')
def spark():
    """
    Create a single Spark Session for all tests.
    FIX: Forces Spark to use the active Virtualenv Python instead of system Python/Windows Store.
    """

    # FIX start
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    # FIX end

    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("CyberTraceTestSuite") \
        .config("spark.sql.shuffle.partitions", "1") \
        .config("spark.ui.enabled", "false") \
        .config("spark.driver.host", "localhost") \
        .config("spark.driver.bindAddress", "localhost") \
        .getOrCreate()
    
    yield spark
    spark.stop()
