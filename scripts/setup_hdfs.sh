#!/bin/bash

# ==========================================
# HDFS SETUP SCRIPT
# Project: Distributed Log Analysis
# User: Saurav Dani
# ==========================================

# 1. Configuration Variables
PROJECT_ROOT="/user/talentum/project_logs"
HADOOP_CMD="hdfs dfs"

# List of all 16 Log Sources
SOURCES=("HDFS" "Hadoop" "Spark" "Zookeeper" "BGL" "HPC" "Windows" "Linux" "Android" "Apache" "OpenStack" "Mac" "OpenSSH" "Thunderbird" "Proxifier" "HealthApp")

echo "=============================================="
echo "Starting Data Lake Construction..."
echo "Root Path: $PROJECT_ROOT"
echo "=============================================="

# 2. Function to safely create a directory
create_dir() {
    DIR_PATH=$1
    echo "Creating: $DIR_PATH"
    $HADOOP_CMD -mkdir -p $DIR_PATH
}

# 3. Create High-Level Zones
create_dir "$PROJECT_ROOT/raw"          # Bronze (Raw Text)
create_dir "$PROJECT_ROOT/refined"      # Silver (Clean Parquet)
create_dir "$PROJECT_ROOT/curated"      # Gold (Aggregated Stats)
create_dir "$PROJECT_ROOT/checkpoints"  # Spark Checkpoints
create_dir "$PROJECT_ROOT/reference"    # CSV Templates/Lookups

# 4. Create Sub-directories for EACH Log Source
# We loop through the list so you don't have to write 32 lines of code
for source in "${SOURCES[@]}"; do
    # Create Raw Input Folder (e.g., /user/talentum/project_logs/raw/HDFS)
    create_dir "$PROJECT_ROOT/raw/$source"
    
    # Create Refined Output Folder (e.g., /user/talentum/project_logs/refined/HDFS)
    create_dir "$PROJECT_ROOT/refined/$source"
done

# 5. Verify the Build
echo "=============================================="
echo "Construction Complete. Verifying Structure:"
echo "=============================================="
$HADOOP_CMD -ls -R $PROJECT_ROOT

echo "Done."
