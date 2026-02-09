import time
import random
import os
import datetime
import sys

# --- CONFIGURATION ---
LOCAL_LANDING_ZONE = "/home/talentum/Distributed-log-analyzer/data/live_stream"
os.makedirs(LOCAL_LANDING_ZONE, exist_ok=True)

# --- FULL TEMPLATES FOR 16 SOURCES ---
LOG_TEMPLATES = {
    "Hadoop": [
        ("INFO", "org.apache.hadoop.mapreduce.v2.app.MRAppMaster: Created MRAppMaster for application appattempt_{id}"),
        ("INFO", "org.apache.hadoop.mapreduce.v2.app.MRAppMaster: Executing with tokens:"),
        ("WARN", "org.apache.hadoop.hdfs.LeaseRenewer: Failed to renew lease for [DFSClient_{id}]"),
        ("ERROR", "org.apache.hadoop.ipc.Client: ConnectionRefused: No route to host from MININT-{id}") 
    ],
    "Apache": [
        ("INFO", "[client 10.10.1.{ip}] GET /index.html HTTP/1.1 200"),
        ("INFO", "[client 10.10.1.{ip}] GET /images/logo.png HTTP/1.1 200"),
        ("ERROR", "[client 10.10.1.{ip}] File does not exist: /var/www/html/admin")
    ],
    "Android": [
        ("I", "ActivityManager: Start proc {id}:com.android.phone/1001 for broadcast"),
        ("D", "dalvikvm: GC_CONCURRENT freed 2048K, 50% free 3000K/6000K, external 0K/0K, paused 2ms+2ms"),
        ("W", "KeyCharacterMap: No keyboard for id {id}"),
        ("E", "AndroidRuntime: FATAL EXCEPTION: main Process: com.android.phone, PID: {id}")
    ],
    "Linux": [
        ("INFO", "sshd[{id}]: Accepted publickey for talentum from 192.168.1.{ip} port 22 ssh2"),
        ("INFO", "systemd: Started Session {id} of user root."),
        ("WARN", "kernel: [12345.67] CPU{id}: Core temperature above threshold, cpu clock throttled"),
        ("ERROR", "sda: Write error: sense key Medium Error")
    ],
    "HDFS": [
        ("INFO", "org.apache.hadoop.hdfs.server.namenode.FSNamesystem: Roll Edit Log from {id}"),
        ("WARN", "org.apache.hadoop.hdfs.server.datanode.DataNode: IOException in offerService"),
        ("ERROR", "org.apache.hadoop.hdfs.server.namenode.NameNode: NameNode is not active. State: STANDBY")
    ],
    "Spark": [
        ("INFO", "org.apache.spark.scheduler.DAGScheduler: Submitting 10 missing tasks from Stage {id}"),
        ("WARN", "org.apache.spark.scheduler.TaskSetManager: Lost task 1.0 in stage {id} (TID {id}, executor 1): ExecutorLostFailure"),
        ("ERROR", "org.apache.spark.deploy.worker.Worker: Failed to connect to master master:7077")
    ],
    # You can add more (Windows, Mac, etc.) following this pattern...
}

def generate_log_line(source_type):
    """Creates a single log line with CURRENT timestamp"""
    # Timestamp formats differ per source, but for simulation we stick to a standard one
    # The Ingestion script handles parsing, so this format must match your Regex in schemas.py
    
    timestamp = datetime.datetime.now()
    
    # Pick a random template (90% normal, 10% error)
    if source_type not in LOG_TEMPLATES:
        return None

    if random.random() > 0.9:
        level, msg_template = LOG_TEMPLATES[source_type][-1] # ERROR
    else:
        # Pick random normal
        level, msg_template = random.choice(LOG_TEMPLATES[source_type][:-1])
        
    # Fill dynamic values
    message = msg_template.format(id=random.randint(1000, 9999), ip=random.randint(10, 99))
    
    # FORMATTING (Must match schemas.py regex!)
    if source_type == "Hadoop":
        # 2015-10-18 18:01:47,978 INFO [main] ...
        ts_str = timestamp.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
        return f"{ts_str} {level} [main] {message}"
        
    elif source_type == "Apache":
        # [Sun Dec 04 04:47:44 2005] [error] ...
        ts_str = timestamp.strftime("%a %b %d %H:%M:%S %Y")
        return f"[{ts_str}] [{level}] {message}"
        
    elif source_type == "Android":
        # 03-17 16:13:38.811 1702 2395 D ...
        ts_str = timestamp.strftime("%m-%d %H:%M:%S.%f")[:-3]
        pid = random.randint(1000, 9999)
        tid = random.randint(1000, 9999)
        return f"{ts_str} {pid} {tid} {level} {message}"
        
    elif source_type == "Linux":
        # Jun 14 15:16:01 combo sshd(pam_unix)[19939]: ...
        ts_str = timestamp.strftime("%b %d %H:%M:%S")
        host = "server" + str(random.randint(1,5))
        proc = "process" + str(random.randint(100,999))
        return f"{ts_str} {host} {proc}: {message}"
        
    elif source_type == "HDFS":
        # 081109 203615 148 INFO ...
        ts_date = timestamp.strftime("%y%m%d")
        ts_time = timestamp.strftime("%H%M%S")
        pid = random.randint(100,999)
        return f"{ts_date} {ts_time} {pid} {level} {message}"

    elif source_type == "Spark":
        # 17/06/09 20:10:40 INFO ...
        ts_str = timestamp.strftime("%y/%m/%d %H:%M:%S")
        return f"{ts_str} {level} {message}"

    return ""

def stream_logs(duration_seconds=60):
    print(f"--- Generating Live Traffic for {duration_seconds} seconds ---")
    start_time = time.time()
    
    # We iterate through ALL defined sources in the dictionary
    sources = list(LOG_TEMPLATES.keys())
    
    while time.time() - start_time < duration_seconds:
        # Pick a random source to simulate (e.g., "Android")
        source = random.choice(sources)
        
        # Write to that specific file
        filename = f"live_{source}_{int(start_time)}.log"
        filepath = os.path.join(LOCAL_LANDING_ZONE, filename)
        
        log_line = generate_log_line(source)
        if log_line:
            with open(filepath, "a") as f: # Append mode
                f.write(log_line + "\n")
            print(f"[{source}] {log_line}")
        
        time.sleep(0.2) # 5 logs per second

if __name__ == "__main__":
    stream_logs(60)
