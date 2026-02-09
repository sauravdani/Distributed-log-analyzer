import time
import subprocess
import os
import glob
import datetime

# ==========================================
# CONFIGURATION
# ==========================================
PROJECT_ROOT = "/home/talentum/Distributed-log-analyzer"
LOCAL_LANDING_ZONE = os.path.join(PROJECT_ROOT, "data", "live_stream")
HDFS_RAW_BASE = "/user/talentum/project_logs/raw"

# Define which sources to process
ACTIVE_SOURCES = ["Hadoop", "Apache", "Android", "Linux", "Spark"]

def run_command(command, description):
    """Helper to run shell commands and print status"""
    print(f"   [EXEC] {description}...")
    try:
        # Run command and hide output unless it fails
        subprocess.check_call(command, shell=True, stdout=subprocess.DEVNULL)
        print(f"   [OK] Success")
    except subprocess.CalledProcessError:
        print(f"   [ERR] Failed (Check logs)")

def pipeline_loop():
    iteration = 1
    
    # Ensure local folder exists
    if not os.path.exists(LOCAL_LANDING_ZONE):
        os.makedirs(LOCAL_LANDING_ZONE)

    while True:
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"\n{'='*50}")
        print(f" PIPELINE RUN #{iteration} | {timestamp}")
        print(f"{'='*50}")

        # 1. GENERATE DATA
        # We simulate traffic for 10 seconds
        print(f"1. Generating Live Logs (10s traffic)...")
        gen_script = os.path.join(PROJECT_ROOT, "scripts", "generate_live_logs.py")
        subprocess.call(f"python3 {gen_script}", shell=True)

        # 2. PROCESS EACH SOURCE
        for source in ACTIVE_SOURCES:
            print(f"\n--- Processing Source: {source} ---")
            
            # Find local files for this source (e.g., live_Apache_*.log)
            # The generator creates files like: live_Apache_1739...log
            local_pattern = os.path.join(LOCAL_LANDING_ZONE, f"*{source}*.log")
            files = glob.glob(local_pattern)
            
            if not files:
                print(f"   [SKIP] No new logs found locally for {source}")
                continue
            
            # A. UPLOAD to HDFS
            # Target: /user/talentum/project_logs/raw/Apache/
            hdfs_target = f"{HDFS_RAW_BASE}/{source}/"
            
            # Ensure HDFS directory exists
            run_command(f"hdfs dfs -mkdir -p {hdfs_target}", "Ensure HDFS Dir")
            
            # Upload
            upload_cmd = f"hdfs dfs -put -f {local_pattern} {hdfs_target}"
            run_command(upload_cmd, f"Upload {len(files)} files to HDFS")
            
            # B. INGEST (Bronze -> Silver)
            ingest_script = os.path.join(PROJECT_ROOT, "spark_jobs", "ingestion", "universal_ingest.py")
            run_command(f"python3 {ingest_script} {source}", "Spark Ingestion")

            # C. ANALYZE (Silver -> Gold)
            trend_script = os.path.join(PROJECT_ROOT, "spark_jobs", "analysis", "calculate_trends.py")
            run_command(f"python3 {trend_script} {source}", "Trend Analysis")

            # D. DETECT ANOMALIES
            anomaly_script = os.path.join(PROJECT_ROOT, "spark_jobs", "analysis", "detect_anomalies.py")
            run_command(f"python3 {anomaly_script} {source}", "Anomaly Detection")

        # 3. CLEANUP
        # Delete local files so we don't re-upload them next time
        print("\n3. Cleaning Local Landing Zone...")
        subprocess.call(f"rm {LOCAL_LANDING_ZONE}/*.log", shell=True)

        print("\n[WAIT] Sleeping for 60 seconds...")
        time.sleep(60)
        iteration += 1

if __name__ == "__main__":
    pipeline_loop()
