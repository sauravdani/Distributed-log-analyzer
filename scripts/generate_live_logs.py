import time
import random
import os
import datetime

# --- CONFIGURATION ---
# Where the live logs will be written locally before upload
LOCAL_LANDING_ZONE = "/home/talentum/Distributed-log-analyzer/data/live_stream"
os.makedirs(LOCAL_LANDING_ZONE, exist_ok=True)

# Define templates to mimic real logs
LOG_TEMPLATES = {
    "Hadoop": [
        ("INFO", "org.apache.hadoop.mapreduce.v2.app.MRAppMaster: Created MRAppMaster for application appattempt_{id}"),
        ("INFO", "org.apache.hadoop.mapreduce.v2.app.MRAppMaster: Executing with tokens:"),
        ("WARN", "org.apache.hadoop.hdfs.LeaseRenewer: Failed to renew lease for [DFSClient_{id}] for 355 seconds"),
        ("ERROR", "org.apache.hadoop.ipc.Client: ConnectionRefused: No route to host from MININT-{id}") # The Anomaly!
    ],
    "Apache": [
        ("INFO", "[client 10.10.1.{ip}] GET /index.html HTTP/1.1 200"),
        ("INFO", "[client 10.10.1.{ip}] GET /images/logo.png HTTP/1.1 200"),
        ("ERROR", "[client 10.10.1.{ip}] File does not exist: /var/www/html/admin") # Anomaly
    ]
}

def generate_log_line(source_type):
    """Creates a single log line with CURRENT timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    
    # Randomly pick a message (90% normal, 10% error)
    if random.random() > 0.9:
        level, msg_template = LOG_TEMPLATES[source_type][-1] # Pick the ERROR one
    else:
        # Pick a random normal one (excluding the last one)
        level, msg_template = random.choice(LOG_TEMPLATES[source_type][:-1])
        
    # Fill in dynamic values
    message = msg_template.format(id=random.randint(1000, 9999), ip=random.randint(10, 99))
    
    # Format matches the Hadoop Regex we defined earlier
    if source_type == "Hadoop":
        return f"{timestamp} {level} [main] {message}"
    elif source_type == "Apache":
        return f"[{timestamp}] [{level}] {message}"
    
    return ""

def stream_logs(duration_seconds=60):
    """Generates logs for a specific duration"""
    print(f"--- Starting Live Log Stream for {duration_seconds} seconds ---")
    start_time = time.time()
    
    # We write to a new file every time so HDFS treats it as a 'new' upload
    filename = f"live_hadoop_{int(start_time)}.log"
    filepath = os.path.join(LOCAL_LANDING_ZONE, filename)
    
    with open(filepath, "w") as f:
        while time.time() - start_time < duration_seconds:
            log_line = generate_log_line("Hadoop")
            f.write(log_line + "\n")
            
            # Print to console so you see it working
            print(log_line)
            
            # Sleep a bit to mimic real traffic (10 logs per second)
            time.sleep(0.1)
            
    print(f"--- Generated {filepath} ---")

if __name__ == "__main__":
    # Generate 1 minute of data
    stream_logs(60)
