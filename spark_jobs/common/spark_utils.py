"""
SHARED SPARK UTILITIES
This module handles Spark Session creation and configuration loading.
"""

import os
import yaml
from pyspark.sql import SparkSession

# --- FIX: Hardcoded Project Root for VM Environment ---
PROJECT_ROOT = "/home/talentum/Distributed-log-analyzer"

def get_spark_session(app_name):
    """
    Creates and returns a SparkSession with optimized settings.
    """
    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .enableHiveSupport() \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark

def load_config(config_path=None):
    """
    Loads the YAML configuration file.
    """
    if not config_path:
        # --- FIX: Use absolute path instead of __file__ ---
        config_path = os.path.join(PROJECT_ROOT, "config", "etl_config.yaml")

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Error loading config from {config_path}: {e}")
        # Only raise if we really can't load it
        raise e
