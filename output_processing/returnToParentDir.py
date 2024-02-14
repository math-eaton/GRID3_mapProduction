import os
import shutil

# Specify the target directory where you want to search for PDFs
target_directory = r'D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\output\20240202'

# Recursively search for PDF files in the target directory
for root, dirs, files in os.walk(target_directory):
    for filename in files:
        if filename.lower().endswith('.pdf'):
            source_path = os.path.join(root, filename)
            # Move the PDF file one level up to the parent directory
            destination_path = os.path.join(os.path.dirname(root), filename)
            shutil.move(source_path, destination_path)

print("files returned to parent directory.")
