import os
import datetime

def is_valid_date(date_str):
    """Check if date_str is in YYYYMMDD format and is a valid date."""
    try:
        datetime.datetime.strptime(date_str, "%Y%m%d")
        return True
    except ValueError:
        return False

def get_base_name_and_date(filename):
    """
    Splits the filename by underscores, and returns:
    - base_name: The part of the name excluding the last underscore segment (assumed to be date)
    - file_date: The YYYYMMDD date as a string
    """
    # Remove extension first
    name, ext = os.path.splitext(filename)
    parts = name.split('_')
    if len(parts) < 2:
        return None, None
    
    file_date = parts[-1]
    if is_valid_date(file_date):
        base_name = '_'.join(parts[:-1])  # join all but the last segment
        return base_name, file_date
    else:
        # If the last segment isn't a valid date, we skip this logic
        return None, None

def main(root_directory):
    # Dictionary to hold:
    # key: (full directory path of the file's folder, base_name)
    # value: (most_recent_file_path, most_recent_date_str)
    found_files = {}

    # Walk through the root directory
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for fname in filenames:
            # Process only .jpg files (if needed, adjust this check)
            if fname.lower().endswith('.jpg'):
                base_name, file_date = get_base_name_and_date(fname)
                
                # If the filename matches the pattern (has a base_name and a valid date)
                if base_name and file_date:
                    key = (dirpath, base_name)
                    file_path = os.path.join(dirpath, fname)
                    
                    if key not in found_files:
                        # Haven't seen this base_name in this folder yet
                        found_files[key] = (file_path, file_date)
                    else:
                        # We have seen this base_name, check if current file is newer
                        existing_file_path, existing_date = found_files[key]
                        if file_date > existing_date:
                            # Current file is newer, update record
                            found_files[key] = (file_path, file_date)
    
    # After we know which files are the newest, we need to delete the older duplicates
    # Let's do another pass through the directories:
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for fname in filenames:
            if fname.lower().endswith('.jpg'):
                base_name, file_date = get_base_name_and_date(fname)
                if base_name and file_date:
                    key = (dirpath, base_name)
                    # Check if this is not the newest file
                    newest_file_path, newest_date = found_files[key]
                    current_file_path = os.path.join(dirpath, fname)
                    if current_file_path != newest_file_path:
                        # This is an older duplicate, delete it
                        print(f"Deleting older file: {current_file_path}")
                        os.remove(current_file_path)

if __name__ == "__main__":
    # Replace with the path to the directory you want to process
    root_dir = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\OUTPUT_A2_reference_20241210\HAUT-KATANGA_REFERENCE"
    main(root_dir)
