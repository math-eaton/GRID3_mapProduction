import os
import zipfile

# Define the input directory containing folders to be compressed
input_directory = r'D:\pathtoDir'

# Iterate through all subdirectories in the input directory
for root, dirs, _ in os.walk(input_directory):
    for folder in dirs:
        # Create a ZIP file for each folder
        folder_path = os.path.join(root, folder)
        zip_filename = os.path.basename(folder_path) + '.zip'
        zip_filepath = os.path.join(root, zip_filename)

        # Create a ZIP archive
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files and subdirectories in the folder to the ZIP archive
            for folder_root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(folder_root, file)
                    # Archive file with its relative path inside the folder
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))

print('compressed all subfolders.')
