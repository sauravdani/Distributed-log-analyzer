"""
LOG SCHEMAS CONFIGURATION
This file maps every log type to a specific Regex Pattern.
Used by: spark_jobs/ingestion/universal_ingest.py
"""

LOG_PATTERNS = {
    # 1. HDFS (Format: 081109 203615 148 INFO ...)
    "HDFS": {
        "pattern": r"^(\d{6}) (\d{6}) (\d+) (\S+) (\S+): (.*)",
        "columns": ["date", "time", "pid", "level", "component", "message"]
    },

    # 2. Hadoop (Format: 2015-10-18 18:01:47,978 INFO [main] ...)
    "Hadoop": {
        "pattern": r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (\S+) \[(.*?)\] (.*?): (.*)",
        "columns": ["timestamp", "level", "thread", "component", "message"]
    },

    # 3. Spark (Format: 17/06/09 20:10:40 INFO ...)
    "Spark": {
        "pattern": r"^(\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) (\S+) (\S+): (.*)",
        "columns": ["timestamp", "level", "component", "message"]
    },

    # 4. Zookeeper (Format: 2015-07-29 17:41:44,747 - INFO ...)
    "Zookeeper": {
        "pattern": r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\S+) \s+\[(.*?)\] - (.*)",
        "columns": ["timestamp", "level", "component", "message"]
    },

    # 5. BGL (BlueGene/L Supercomputer)
    "BGL": {
        "pattern": r"^(\S+) (\d{4}\.\d{2}\.\d{2}) (\S+) (\d{4}-\d{2}-\d{2}-\d{2}\.\d{2}\.\d{2}\.\d{6}) (\S+) (\S+) (\S+) (.*)",
        "columns": ["alert_flag", "date", "node", "timestamp", "node_repeat", "component", "level", "message"]
    },

    # 6. HPC (High Performance Computing)
    "HPC": {
        "pattern": r"^(\d+) (\S+) (\S+) (\S+) (\d+) (\d+) (.*)",
        "columns": ["log_id", "node", "component", "state", "time_unix", "level", "message"]
    },

    # 7. Windows (Format: 2016-09-28 04:30:30, Info CBS ...)
    "Windows": {
        "pattern": r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}), (\S+)\s+(\S+)\s+(.*)",
        "columns": ["timestamp", "level", "component", "message"]
    },

    # 8. Linux (Syslog format)
    "Linux": {
        "pattern": r"^([A-Z][a-z]{2}\s+\d+\s\d{2}:\d{2}:\d{2}) (\S+) (\S+): (.*)",
        "columns": ["timestamp_str", "host", "process", "message"]
    },

    # 9. Android (Format: 03-17 16:13:38.811 1702 2395 D ...)
    "Android": {
        "pattern": r"^(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})\s+(\d+)\s+(\d+)\s+(\S)\s+(\S+): (.*)",
        "columns": ["timestamp", "pid", "tid", "level_code", "component", "message"]
    },

    # 10. Apache (Web Server)
    "Apache": {
        "pattern": r"^\[(.*?)\] \[(.*?)\] (.*)",
        "columns": ["timestamp", "level", "message"]
    },

    # 11. OpenStack (Cloud)
    "OpenStack": {
        "pattern": r"^(\S+) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) (\d+) (\S+) (.*)",
        "columns": ["log_file", "timestamp", "pid", "level", "message"]
    },

    # 12. Mac (Apple System Logs)
    "Mac": {
        "pattern": r"^([A-Z][a-z]{2}\s+\d+\s\d{2}:\d{2}:\d{2}) (\S+) (\S+): (.*)",
        "columns": ["timestamp_str", "host", "process", "message"]
    },

    # 13. OpenSSH (Secure Shell)
    "OpenSSH": {
        "pattern": r"^([A-Z][a-z]{2}\s+\d+\s\d{2}:\d{2}:\d{2}) (\S+) (\S+): (.*)",
        "columns": ["timestamp_str", "host", "process", "message"]
    },

    # 14. Thunderbird (Supercomputer)
    "Thunderbird": {
        "pattern": r"^- (\d+) (\d{4}\.\d{2}\.\d{2}) (\S+) (.*)",
        "columns": ["timestamp_unix", "date", "host", "message"]
    },

    # 15. Proxifier (Proxy Logs)
    "Proxifier": {
        "pattern": r"^\[(\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\] (\S+) - (.*)",
        "columns": ["timestamp", "program", "message"]
    },

    # 16. HealthApp (Mobile App)
    "HealthApp": {
        "pattern": r"^([^|]+)\|([^|]+)\|([^|]+)\|(.*)",
        "columns": ["timestamp", "component", "pid", "message"]
    }
}
