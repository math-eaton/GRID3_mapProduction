
import subprocess
import os
import shutil
import sys
import concurrent.futures
from datetime import datetime

# Define the number of instances and the paths to the scripts
num_instances = 4
current_dir = os.path.dirname(os.path.abspath(__file__))
export_script_path = os.path.join(current_dir, "exportMapSeries.py")
count_script_path = os.path.join(current_dir, "count_matching_pages.py")
original_project_path = r"E:\mheaton\cartography\COD_microplanning_042024\COD_microplanning_052024.aprx"

def get_current_date_format():
    return datetime.now().strftime('%Y%m%d')

def create_temp_project_file(instance_id):
    temp_project_path = os.path.join(os.path.dirname(original_project_path), f"temp_{instance_id}_{get_current_date_format()}.aprx")
    shutil.copyfile(original_project_path, temp_project_path)
    return temp_project_path

# Print paths for debugging
print(f"Export script path: {export_script_path}")
print(f"Count script path: {count_script_path}")
print(f"Original project path: {original_project_path}")

# Step 1: Count the total number of matching pages
print(f"Running count script: {count_script_path}")
result = subprocess.run([sys.executable, count_script_path], capture_output=True, text=True)
print(f"Count script stdout: {result.stdout}")
print(f"Count script stderr: {result.stderr}")

try:
    total_pages = int(result.stdout.strip())
    if total_pages < 0:
        raise ValueError("Counting matching pages failed.")
except ValueError as e:
    print(f"Failed to count matching pages: {e}")
    sys.exit(1)

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
    command = [sys.executable, export_script_path, str(start_page), str(end_page), temp_project_path]
    commands.append(command)
    start_page = end_page + 1

# Function to run a command and log its output
def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr

# Run the commands in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=num_instances) as executor:
    futures = {executor.submit(run_command, cmd): cmd for cmd in commands}
    for future in concurrent.futures.as_completed(futures):
        cmd = futures[future]
        try:
            stdout, stderr = future.result()
            print(f"Command: {' '.join(cmd)}")
            print(f"stdout: {stdout.decode()}")
            print(f"stderr: {stderr.decode()}")
        except Exception as exc:
            print(f"Command {cmd} generated an exception: {exc}")

# Clean up the temporary project files
for i in range(num_instances):
    temp_project_path = os.path.join(os.path.dirname(original_project_path), f"temp_{i}_{get_current_date_format()}.aprx")
    os.remove(temp_project_path)
