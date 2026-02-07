#!/bin/bash

# ==========================================
# SMART UPLOAD SCRIPT
# Project: Distributed Log Analysis
# User: Saurav Dani
# ==========================================

# 1. Configuration
# We assume this script is running from the 'scripts' folder, 
# so the data is one level up in 'data'
LOCAL_DATA_DIR="$(dirname "$0")/../data"
HDFS_ROOT="/user/talentum/project_logs"

# List of known sources (Must match the folders created in setup_hdfs.sh)
SOURCES=("HDFS" "Hadoop" "Spark" "Zookeeper" "BGL" "HPC" "Windows" "Linux" "Android" "Apache" "OpenStack" "Mac" "OpenSSH" "Thunderbird" "Proxifier" "HealthApp")

echo "=============================================="
echo "Starting Smart Upload..."
echo "Source Local Dir: $LOCAL_DATA_DIR"
echo "Target HDFS Root: $HDFS_ROOT"
echo "=============================================="

# 2. Loop through each Source Type
for source in "${SOURCES[@]}"; do
    
    # Define the pattern to look for (e.g., "Hadoop*.log")
    # This matches "Hadoop_2k.log", "Hadoop_v2.log", etc.
    LOG_PATTERN="$LOCAL_DATA_DIR/${source}*.log"
    
    # Check if any files exist matching this pattern
    # ls matches the pattern, 2>/dev/null hides errors if no files found
    if ls $LOG_PATTERN 1> /dev/null 2>&1; then
        
        echo "--> Found logs for: $source"
        
        # Upload to the specific HDFS folder
        # -f forces overwrite if file exists
        hdfs dfs -put -f $LOG_PATTERN "$HDFS_ROOT/raw/$source/"
        
        if [ $? -eq 0 ]; then
             echo "    [SUCCESS] Uploaded to $HDFS_ROOT/raw/$source/"
        else
             echo "    [ERROR] Failed to upload $source"
        fi
        
    else
        echo "--> No logs found locally for: $source (Skipping)"
    fi

done

# 3. Handle CSV Templates (Reference Data)
# If you have CSV files (like Hadoop_templates.csv), put them in reference
CSV_PATTERN="$LOCAL_DATA_DIR/*.csv"
if ls $CSV_PATTERN 1> /dev/null 2>&1; then
    echo "=============================================="
    echo "Uploading Reference CSVs..."
    hdfs dfs -put -f $CSV_PATTERN "$HDFS_ROOT/reference/"
    echo "    [SUCCESS] CSVs uploaded to $HDFS_ROOT/reference/"
fi

echo "=============================================="
echo "Upload Complete."
echo "=============================================="
