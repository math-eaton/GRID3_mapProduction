import subprocess
import os
import shutil
from datetime import datetime

# Define the number of instances and the path to the export script
num_instances = 4
export_script_path = "exportMapSeries.py"
original_project_path = r"E:\mheaton\cartography\COD_microplanning_042024\COD_microplanning_052024.aprx"

def get_current_date_format():
    return datetime.now().strftime('%Y%m%d')

def create_temp_project_file(instance_id):
    temp_project_path = os.path.join(os.path.dirname(original_project_path), f"temp_{instance_id}_{get_current_date_format()}.aprx")
    shutil.copyfile(original_project_path, temp_project_path)
    return temp_project_path

# Step 1: Count the total number of matching pages
result = subprocess.run(["python", "count_matching_pages.py"], capture_output=True, text=True)
total_pages = int(result.stdout.strip())

# Step 2: Divide the total pages into chunks and run the instances
pages_per_instance = total_pages // num_instances
remainder = total_pages % num_instances

# Create commands for each instance
commands = []
start_page = 1

for i in range(num_instances):
    end_page = start_page + pages_per_instance - 1
    if i == num_instances - 1:  # Add the remainder to the last instance
        end_page += remainder

    temp_project_path = create_temp_project_file(i)
    command = ["python", export_script_path, str(start_page), str(end_page), temp_project_path]
    commands.append(command)
    start_page = end_page + 1

# Run the commands in parallel
processes = [subprocess.Popen(command) for command in commands]

# Wait for all processes to finish
for process in processes:
    process.communicate()

# Clean up the temporary project files
for i in range(num_instances):
    temp_project_path = os.path.join(os.path.dirname(original_project_path), f"temp_{i}_{get_current_date_format()}.aprx")
    os.remove(temp_project_path)
