import time
import subprocess
import os
import glob

# --- CONFIGURATION ---
PROJECT_ROOT = "/home/talentum/Distributed-log-analyzer"
LOCAL_LANDING_ZONE = f"{PROJECT_ROOT}/data/live_stream"
HDFS_BASE = "/user/talentum/project_logs/raw"

# Define which sources to process (Must match the Generator keys)
ACTIVE_SOURCES = ["Hadoop", "Apache", "Android", "Linux", "Spark", "HDFS"]

def run_command(command, description):
    print(f"   [EXEC] {description}...")
    try:
        subprocess.check_call(command, shell=True)
        print(f"   [OK] Success")
    except subprocess.CalledProcessError:
        print(f"   [ERR] Failed (Ignoring)")

def pipeline_loop():
    iteration = 1
    while True:
        print(f"\n{'='*50}")
        print(f" PIPELINE RUN #{iteration} | {time.strftime('%H:%M:%S')}")
        print(f"{'='*50}")

        # 1. GENERATE DATA (Simulate traffic for all sources)
        print(f"1. Generating Live Logs (10 seconds)...")
        subprocess.call(f"python3 {PROJECT_ROOT}/scripts/generate_live_logs.py", shell=True)

        # 2. UPLOAD & PROCESS (Loop through each source)
        for source in ACTIVE_SOURCES:
            print(f"\n--- Processing Source: {source} ---")
            
            # Pattern to find specific logs (e.g., live_Apache_*.log)
            local_pattern = f"{LOCAL_LANDING_ZONE}/*{source}*.log"
            
            # Check if we actually have files for this source
            files = glob.glob(local_pattern)
            if not files:
                print(f"   [SKIP] No new logs for {source}")
                continue
                
            # A. Upload to specific HDFS folder (e.g., /raw/Apache/)
            hdfs_target = f"{HDFS_BASE}/{source}/"
            run_command(f"hdfs dfs -put -f {local_pattern} {hdfs_target}", f"Upload to HDFS {source}")
            
            # B. Ingest (Bronze -> Silver)
            run_command(f"python3 {PROJECT_ROOT}/spark_jobs/ingestion/universal_ingest.py {source}", f"Spark Ingest {source}")

            # C. Analyze (Silver -> Gold)
            run_command(f"python3 {PROJECT_ROOT}/spark_jobs/analysis/calculate_trends.py {source}", f"Calculate Trends {source}")

            # D. Detect Anomalies
            run_command(f"python3 {PROJECT_ROOT}/spark_jobs/analysis/detect_anomalies.py {source}", f"Detect Anomalies {source}")

        # 3. CLEANUP (Delete local files so we don't re-upload them next time)
        print("\n3. Cleaning Local Landing Zone...")
        run_command(f"rm {LOCAL_LANDING_ZONE}/*.log", "Delete Local Files")

        print("\n[WAIT] Sleeping for 60 seconds...")
        time.sleep(60)
        iteration += 1

if __name__ == "__main__":
    pipeline_loop()
