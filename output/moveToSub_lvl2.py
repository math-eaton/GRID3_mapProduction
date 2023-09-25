import os
import shutil

folder = r'D:\xyz'

# Get a list of all PDF files in the folder
pdf_files = [file for file in os.listdir(folder) if file.lower().endswith('.pdf')]

# Iterate through each PDF file and organize them into subfolders
for pdf_file in pdf_files:
    # Extract the target folder name based on the delimiter ('_') ... adjust the index value based on intended split level
    target = pdf_file.split('_')[4]
    
    # Create the target directory if it doesn't exist
    target_directory = os.path.join(folder, target)
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    # Move the PDF file to the target directory
    source_path = os.path.join(folder, pdf_file)
    destination_path = os.path.join(target_directory, pdf_file)
    shutil.move(source_path, destination_path)

print("done.")
