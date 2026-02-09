import time
import subprocess
import os

# --- CONFIGURATION ---
PROJECT_ROOT = "/home/talentum/Distributed-log-analyzer"
HDFS_RAW = "/user/talentum/project_logs/raw/Hadoop"

def run_command(command, step_name):
    print(f"\n[ORCHESTRATOR] Starting Step: {step_name}...")
    try:
        # Run the command in the shell
        subprocess.check_call(command, shell=True)
        print(f"[ORCHESTRATOR] ✔ Success: {step_name}")
    except subprocess.CalledProcessError as e:
        print(f"[ORCHESTRATOR] ✘ Failed: {step_name}")
        # We don't stop the loop, just this iteration
        pass

def pipeline_loop():
    iteration = 1
    while True:
        print(f"\n{'='*40}")
        print(f" PIPELINE RUN #{iteration} | Time: {time.strftime('%H:%M:%S')}")
        print(f"{'='*40}")

        # 1. GENERATE DATA (Simulate 10 seconds of traffic)
        # We run the generator for just 10 seconds so the pipeline moves fast
        run_command(f"python3 {PROJECT_ROOT}/scripts/generate_live_logs.py", "Generate Live Logs")

        # 2. UPLOAD TO HDFS
        run_command(f"hdfs dfs -put -f {PROJECT_ROOT}/data/live_stream/*.log {HDFS_RAW}/", "Upload to HDFS")
        
        # 3. CLEANUP LOCAL FILES
        run_command(f"rm {PROJECT_ROOT}/data/live_stream/*.log", "Cleanup Local Landing Zone")

        # 4. INGEST (Bronze -> Silver)
        run_command(f"python3 {PROJECT_ROOT}/spark_jobs/ingestion/universal_ingest.py Hadoop", "Spark Ingestion")

        # 5. ANALYZE (Silver -> Gold)
        run_command(f"python3 {PROJECT_ROOT}/spark_jobs/analysis/calculate_trends.py Hadoop", "Trend Analysis")

        # 6. DETECT ANOMALIES
        run_command(f"python3 {PROJECT_ROOT}/spark_jobs/analysis/detect_anomalies.py Hadoop", "Anomaly Detection")

        print("\n[ORCHESTRATOR] Sleeping for 60 seconds...")
        time.sleep(60)
        iteration += 1

if __name__ == "__main__":
    # Ensure local directory exists
    os.makedirs(f"{PROJECT_ROOT}/data/live_stream", exist_ok=True)
    pipeline_loop()
