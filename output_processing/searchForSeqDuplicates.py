import os
import shutil

def move_matching_files(primary_dir, secondary_dir):
    # Ensure the "delete" subfolder exists
    delete_dir = os.path.join(primary_dir, "multipart")
    if not os.path.exists(delete_dir):
        os.makedirs(delete_dir)

    # List all files in the primary and secondary directories
    primary_files = {f: os.path.splitext(f)[0] for f in os.listdir(primary_dir) if os.path.isfile(os.path.join(primary_dir, f))}
    secondary_files = {os.path.splitext(f)[0] for f in os.listdir(secondary_dir) if os.path.isfile(os.path.join(secondary_dir, f))}

    # Compare and move files
    for file, primary_base in primary_files.items():
        # Check if a file exists in the secondary directory that matches the primary file name excluding any two-character suffix
        if any(secondary_base for secondary_base in secondary_files if primary_base == secondary_base[:-2]):
            # Move the file to the "delete" subfolder
            shutil.move(os.path.join(primary_dir, file), os.path.join(delete_dir, file))
            print(f"Moved '{file}' to the 'multipart' folder.")

# Example usage
primary_dir = r'D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\output\20240202'
secondary_dir = r'D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\output\20240210'
move_matching_files(primary_dir, secondary_dir)
