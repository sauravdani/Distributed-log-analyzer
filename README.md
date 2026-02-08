# Distributed Log Analysis System 🚀

**Author:** Saurav Dani  
**Tech Stack:** Hadoop HDFS, PySpark, Apache Airflow, Python, Machine Learning (Isolation Forest/Z-Score)

---

## 📖 Project Overview

This project is an end-to-end **Big Data Pipeline** designed to ingest, process, and analyze massive volumes of system logs from diverse sources (Hadoop, Apache, Android, etc.).

It solves the problem of "Log Fatigue" by automating the transformation of unstructured text logs into structured insights. The system features a **Universal Ingestion Engine**, a **Real-Time Anomaly Detection System**, and a **Live Data Simulator** to mimic high-velocity server traffic.

---

## 🏗 Architecture (Medallion Pattern)

The data flows through a structured **Data Lake** architecture on HDFS:

1.  **Bronze Layer (Raw)**:  
    * **Input:** Raw text logs (`.log`) from 16+ different sources.
    * **Storage:** `/user/talentum/project_logs/raw/`
    * **Process:** Direct ingestion via `hdfs dfs -put` or Live Stream Generator.

2.  **Silver Layer (Refined)**:  
    * **Transformation:** Parsing unstructured text using **Regex** into structured columns (`timestamp`, `level`, `component`, `message`).
    * **Storage:** `/user/talentum/project_logs/refined/` (Parquet format).
    * **Engine:** PySpark Ingestion Job.

3.  **Gold Layer (Curated)**:  
    * **Transformation:** Aggregating metrics (Error Rates, Warning Counts) over time windows (e.g., 1 minute).
    * **Storage:** `/user/talentum/project_logs/curated/`
    * **Analytics:** Anomaly Detection (Statistical Z-Score Analysis) to flag spikes in error rates.

---

## 📂 Project Structure

```text
Distributed-log-analyzer/
│
├── config/                     # Configuration Center
│   ├── schemas.py              # Regex patterns for 16+ log types
│   └── etl_config.yaml         # Central paths and thresholds
│
├── dags/                       # Automation
│   ├── log_ingestion_dag.py    # Airflow DAG for batch processing
│   └── live_stream_dag.py      # Airflow DAG for continuous live streaming
│
├── spark_jobs/                 # Core Processing Logic
│   ├── common/                 # Shared utilities (SparkSession, Config Loader)
│   ├── ingestion/              # Bronze -> Silver logic
│   │   └── universal_ingest.py # The Generic Parser
│   └── analysis/               # Silver -> Gold logic
│       ├── calculate_trends.py # Aggregation Engine
│       └── detect_anomalies.py # Machine Learning Engine
│
├── scripts/                    # Helper Scripts
│   ├── setup_hdfs.sh           # Builds the Data Lake folders
│   ├── upload_samples.sh       # Pushes local data to HDFS
│   └── generate_live_logs.py   # Simulates a live server attack
│
├── notebooks/                  # Interactive Development
│   ├── Ingestion_Layer.ipynb   # Dev notebook for parsing
│   ├── Calculate_Trends.ipynb  # Dev notebook for aggregation
│   └── Anomaly_Detection.ipynb # Dev notebook for ML
│
└── data/                       # Local Landing Zone for logs
