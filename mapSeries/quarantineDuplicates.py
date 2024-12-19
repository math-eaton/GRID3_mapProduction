import os
import re
import shutil

# Directory containing the files
base_directory = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\OUTPUT_A2_reference_20241210\HAUT-KATANGA_REFERENCE"  # Change this to your directory

# Create the delete subfolder if it does not exist
delete_folder = os.path.join(base_directory, "delete")
if not os.path.exists(delete_folder):
    os.makedirs(delete_folder)

# Regex to find files that have text after YYYYMMDD
# This looks for any sequence of 8 digits (the date) followed by an underscore and something else
pattern = re.compile(r"\d{8}_.+")  # Matches YYYYMMDD_ and then additional characters

for filename in os.listdir(base_directory):
    filepath = os.path.join(base_directory, filename)

    # Skip directories
    if os.path.isdir(filepath):
        continue

    # Check if filename matches the pattern (i.e., has text after the 8-digit date)
    if pattern.search(filename):
        # Move the file to the delete subfolder
        new_path = os.path.join(delete_folder, filename)
        shutil.move(filepath, new_path)
        print(f"Moved: {filename} -> {new_path}")
    else:
        # Filename is either doesn't contain a date or doesn't have text after it
        # So we do nothing
        pass

print("Done.")
