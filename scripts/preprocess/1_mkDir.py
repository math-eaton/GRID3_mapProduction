import os
import arcpy
import argparse
from datetime import datetime

arcpy.env.overwriteOutput = True

def create_directory(path):
    """Helper function to create a directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)
    print(f"Created directory: {path}")

def create_file_geodatabase(folder_path, gdb_name):
    """Helper function to create a file geodatabase using ArcPy."""
    gdb_path = os.path.join(folder_path, gdb_name)
    if not arcpy.Exists(gdb_path):
        arcpy.management.CreateFileGDB(folder_path, gdb_name)
        print(f"Created file geodatabase: {gdb_path}")
    else:
        print(f"File geodatabase already exists: {gdb_path}")

def create_full_project(base_dir):
    """Creates the full directory structure."""
    print("\nSetting up FULL PROJECT...")
    # Define the static structure
    structure = {
        "data": [], 
        "output": ["temp", "archive"],
        # "scripts": [],
        # "docs": [],
        # "logs": [],
        # "config": []
    }

    # Create base directories
    create_directory(base_dir)

    for folder, subfolders in structure.items():
        folder_path = os.path.join(base_dir, folder)
        create_directory(folder_path)
        for subfolder in subfolders:
            create_directory(os.path.join(folder_path, subfolder))

    # Create an initial timestamped data subfolder
    add_new_data_folder(base_dir)
    print("\nFULL PROJECT setup complete!")

def add_new_data_folder(base_dir):
    """Adds a new timestamped data subfolder."""
    print("\nAdding NEW INPUT...")
    data_path = os.path.join(base_dir, "data")
    create_directory(data_path)

    # Generate the initial date-based folder name
    date_str = datetime.now().strftime("%Y%m%d")
    timestamped_folder = os.path.join(data_path, date_str)

    # Check if the folder already exists
    if os.path.exists(timestamped_folder):
        # Append time to avoid duplication
        time_str = datetime.now().strftime("%H%M%S")
        timestamped_folder = os.path.join(data_path, f"{date_str}_{time_str}")

    # Define subfolders and geodatabases for the timestamped folder
    subfolders = {
        "input": "input.gdb",
        "scratch": "scratch.gdb",
        "processed": "processed.gdb"
    }

    # Create the timestamped folder and its contents
    create_directory(timestamped_folder)
    for folder_name, gdb_name in subfolders.items():
        folder_path = os.path.join(timestamped_folder, folder_name)
        create_directory(folder_path)
        create_file_geodatabase(folder_path, gdb_name)

    print(f"NEW INPUT added under: {timestamped_folder}")

# Main execution logic
if __name__ == "__main__":
    # Define project root
    #todo: refactor for argparse
    # print("Project root?")
    # parser.add_argument('filename')
    project_root = "E:\mheaton\cartography\GRID_2025\RDC_EAF_2025"

    # Choose action
    print("Choose setup option:")
    print("1 - Full Project Setup")
    print("2 - Add New Input Data Folder")

    choice = input("Enter your choice (1 or 2): ").strip()
    if choice == "1":
        create_full_project(project_root)
    elif choice == "2":
        add_new_data_folder(project_root)
    else:
        print("Invalid choice. Exiting.")
