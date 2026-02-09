from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

# --- CONFIG ---
PROJECT_ROOT = "/home/talentum/Distributed-log-analyzer"
HDFS_RAW_PATH = "/user/talentum/project_logs/raw/Hadoop"
LOCAL_LANDING_ZONE = f"{PROJECT_ROOT}/data/live_stream"

default_args = {
    'owner': 'talentum',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 0,
}

# Run every 5 minutes
with DAG('03_live_stream_pipeline',
         default_args=default_args,
         schedule_interval='*/5 * * * *',
         catchup=False,
         tags=['live', 'streaming']) as dag:

    # 1. GENERATE DUMMY DATA (Simulate the Server)
    # In a real world, this happens on the server. Here, we force it.
    generate_data = BashOperator(
        task_id='simulate_server_logs',
        bash_command=f"python3 {PROJECT_ROOT}/scripts/generate_live_logs.py"
    )

    # 2. UPLOAD TO HDFS (The "Flume" Replacement)
    # Moves the generated file to HDFS and deletes the local copy to save space
    upload_to_hdfs = BashOperator(
        task_id='push_to_data_lake',
        bash_command=f"hdfs dfs -put {LOCAL_LANDING_ZONE}/*.log {HDFS_RAW_PATH}/ && rm {LOCAL_LANDING_ZONE}/*.log"
    )

    # 3. RUN INGESTION (Bronze -> Silver)
    ingest_silver = SparkSubmitOperator(
        task_id='spark_ingest',
        application=f"{PROJECT_ROOT}/spark_jobs/ingestion/universal_ingest.py",
        application_args=["Hadoop"],
        conn_id="spark_default",
        conf={"spark.master": "local[*]"}
    )

    # 4. RUN ANALYSIS (Silver -> Gold)
    analyze_gold = SparkSubmitOperator(
        task_id='spark_analyze',
        application=f"{PROJECT_ROOT}/spark_jobs/analysis/calculate_trends.py",
        application_args=["Hadoop"],
        conn_id="spark_default",
        conf={"spark.master": "local[*]"}
    )

    # Define Workflow
    generate_data >> upload_to_hdfs >> ingest_silver >> analyze_gold
