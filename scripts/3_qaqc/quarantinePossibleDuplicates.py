import os
import sys
import shutil
import re

def quarantine_files_with_suffix(directory):
    """
    Move any file in 'directory' that has an 8-digit date followed by an underscore 
    and some suffix before the extension into a 'delete' subdirectory.
    
    For example:
    - xyz_abc_20241215_1.jpg -> quarantined (has suffix "_1" after the date)
    - xyz_abc_20241215.jpg   -> not quarantined (no suffix after date)
    """
    # Create the 'delete' subdirectory if it doesn't exist
    quarantine_dir = os.path.join(directory, "delete")
    if not os.path.exists(quarantine_dir):
        os.makedirs(quarantine_dir)
    
    # Compile a regex pattern to identify files with a suffix after YYYYMMDD
    # This pattern:
    #  - Looks for one or more characters, then underscore,
    #  - followed by 8 digits (the date), 
    #  - followed by an underscore and then one or more characters (the suffix)
    #
    # Example match: "..._20241215_1"
    pattern = re.compile(r".*_\d{8}_.+")
    
    for filename in os.listdir(directory):
        # Skip the 'delete' folder
        if filename == "delete":
            continue
        
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path):
            base, ext = os.path.splitext(filename)
            
            # Check if this filename matches our pattern (has date + suffix)
            if pattern.match(base):
                target_path = os.path.join(quarantine_dir, filename)
                print(f"Quarantining {file_path} -> {target_path}")
                shutil.move(file_path, target_path)

if __name__ == "__main__":
    # Example usage:
    # python quarantine_files.py /path/to/directory
    if len(sys.argv) > 1:
        target_directory = sys.argv[1]
    else:
        # Define your directory path here if not using command line arguments
        target_directory = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\OUTPUT_A2_reference_20241215"
    
    quarantine_files_with_suffix(target_directory)
