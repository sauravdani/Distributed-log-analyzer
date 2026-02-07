
#########################################################################################
# 
# Project Flow
# 
#########################################################################################

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
