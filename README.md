Here is a professional README.md file for your project. This document serves as the "Front Page" of your GitHub repository and explains exactly what you built to recruiters and reviewers.

Create a file named README.md in your project root (/home/talentum/Distributed-log-analyzer/README.md) and paste the content below.

Distributed Log Analysis System 🚀
Author: Saurav Dani

Tech Stack: Hadoop HDFS, PySpark, Apache Airflow, Python, Machine Learning (Isolation Forest/Z-Score)

📖 Project Overview
This project is an end-to-end Big Data Pipeline designed to ingest, process, and analyze massive volumes of system logs from diverse sources (Hadoop, Apache, Android, etc.).

It solves the problem of "Log Fatigue" by automating the transformation of unstructured text logs into structured insights. The system features a Universal Ingestion Engine, a Real-Time Anomaly Detection System, and a Live Data Simulator to mimic high-velocity server traffic.

🏗 Architecture (Medallion Pattern)
The data flows through a structured Data Lake architecture on HDFS:

Bronze Layer (Raw):

Input: Raw text logs (.log) from 16+ different sources.

Storage: /user/talentum/project_logs/raw/

Process: Direct ingestion via hdfs dfs -put or Live Stream Generator.

Silver Layer (Refined):

Transformation: Parsing unstructured text using Regex into structured columns (timestamp, level, component, message).

Storage: /user/talentum/project_logs/refined/ (Parquet format).

Engine: PySpark Ingestion Job.

Gold Layer (Curated):

Transformation: Aggregating metrics (Error Rates, Warning Counts) over time windows (e.g., 1 minute).

Storage: /user/talentum/project_logs/curated/

Analytics: Anomaly Detection (Statistical Z-Score Analysis) to flag spikes in error rates.

📂 Project Structure
Plaintext
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
⚙️ Setup & Installation
1. Prerequisites
Hadoop (HDFS & YARN) must be running (start-all.sh).

Python 3.6+ with PySpark installed.

Apache Airflow (Optional for orchestration).

2. Configure Environment
Update config/etl_config.yaml if your HDFS path differs:

YAML
project:
  base_path: "/user/talentum/project_logs"
3. Build the Data Lake
Run the setup script to create the HDFS directory structure:

Bash
chmod +x scripts/setup_hdfs.sh
./scripts/setup_hdfs.sh
4. Upload Data
Place your .log files in the data/ folder and run:

Bash
chmod +x scripts/upload_samples.sh
./scripts/upload_samples.sh
🚀 How to Run the Pipeline
Option A: Interactive (Jupyter Notebooks)
Navigate to the notebooks/ folder and run them in order:

Ingestion_Layer.ipynb: Converts Raw Text -> Parquet (Silver).

Calculate_Trends.ipynb: Calculates Error Rates -> Parquet (Gold).

Anomaly_Detection.ipynb: Detects spikes and prints alerts.

Option B: Command Line (Production Style)
Bash
# Step 1: Ingest Hadoop Logs
python spark_jobs/ingestion/universal_ingest.py Hadoop

# Step 2: Calculate Trends
python spark_jobs/analysis/calculate_trends.py Hadoop

# Step 3: Check for Anomalies
python spark_jobs/analysis/detect_anomalies.py Hadoop
Option C: Live Simulation (The "Wow" Factor)
Start the Live Generator in one terminal:

Bash
python scripts/generate_live_logs.py
Trigger the Airflow DAG 03_live_stream_pipeline to automatically ingest and analyze the incoming data stream every 5 minutes.

📊 Key Features
Universal Parser: One script handles 16 different log formats (Linux, Windows, Hadoop, Spark, etc.) using a configuration-driven approach.

Scalable: Built on PySpark, capable of handling Terabytes of logs.

Resilient: Handles messy data, missing timestamps, and schema variations.

Intelligent: Uses statistical analysis (Z-Score) to automatically detect when system error rates deviate from the norm (e.g., DDoS attacks or outages).


#######################################################################################
# 
# Project Flow
# 
#######################################################################################

1. First step it to get the requinments and install them using the requirnemnts.txt using: 
	pip install -r /home/talentum/Distributed-log-analyzer/requirements.txt.

   Faced some errors in installing the requirnments so did this to fix them
	
	# 1. Unset the variable causing the conflict
	unset PYTHONPATH

	# 2. Create a clean Conda environment specifically for this project
	conda create -n log_project python=3.8 -y

	# 3. Activate it
	conda activate log_project

	# 4. Now install the requirements
	pip install -r /home/talentum/Distributed-log-analyzer/requirements.txt

2. Writing config/schema.py file to descripe how to read all the logs and how are interpreted.
	
3. setting up hdfs using setup_hdfs.sh script

4. Now uploading all the required files from shared to hdfs. making 'upload_script.sh' to do so.

5. Now making utils for spark. inetializing all the required context and starting points required in spark.

6. now made a notebook directory in the main project directory. inside that created a 'ingestion_layer.ipynb' to handle the data ingestion to make in 
