class ProjectConfig:
    STORAGE_ACCOUNT = "cybertracebronze"
    CONTAINER_NAME = "bronze"
    SCOPE_NAME = "cybertrace-secrets"
    KEY_NAME = "storage-access-key"

    @staticmethod
    def get_base_path():
        return f"abfss://{ProjectConfig.CONTAINER_NAME}@{ProjectConfig.STORAGE_ACCOUNT}.dfs.core.windows.net"


class Paths:
    BASE_PATH = ProjectConfig.get_base_path()
    RAW_LOGS = f"{BASE_PATH}/raw_logs"
    SCHEMA = f"{BASE_PATH}/schemas/ingestion_schema"
    CHECKPOINT_BASE = f"{BASE_PATH}/checkpoints"
    CHECKPOINT_BRONZE = f"{BASE_PATH}/checkpoints/bronze_mordor_logs"
    CHECKPOINT_SILVER = f"{BASE_PATH}/checkpoints/silver_mordor_logs"
    GOLD = f"{BASE_PATH}/gold/threat_stats"
    QUARANTINE = f"{BASE_PATH}/_quarantine"



def setup_authentication(spark, dbutils):
    """Authenticates Spark session to ADLS via Key Vault."""
    try:
        key = dbutils.secrets.get(scope=ProjectConfig.SCOPE_NAME, key=ProjectConfig.KEY_NAME)
        spark.conf.set(
            f"fs.azure.account.key.{ProjectConfig.STORAGE_ACCOUNT}.dfs.core.windows.net",
            key
        )
        print("AUTH: Connected to ADLS Gen2")
    except Exception as e:
        raise RuntimeError(f"AUTH ERROR: Failed to connect to ADLS Gen2: {e}")