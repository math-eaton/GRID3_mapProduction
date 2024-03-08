import os
import shutil

def organize_pdfs_in_subfolders(folder):
    # Walk through all folders and subfolders
    for root, dirs, files in os.walk(folder):
        # Filter for PDF files
        pdf_files = [file for file in files if file.lower().endswith('.pdf')]
        
        # If there are PDF files, organize them
        if pdf_files:
            for pdf_file in pdf_files:
                # Extract the target folder name based on the delimiter ('_')
                # Adjust the index value based on intended split level
                try:
                    target = pdf_file.split('_')[3]
                except IndexError:
                    # Handle case where filename does not contain enough parts to split
                    print(f"Skipping {pdf_file}: cannot extract target folder from filename")
                    continue
                
                # The target directory is now created within the root directory
                target_directory = os.path.join(root, target)
                if not os.path.exists(target_directory):
                    os.makedirs(target_directory)
                
                # Move the PDF file to the target directory
                source_path = os.path.join(root, pdf_file)
                destination_path = os.path.join(target_directory, pdf_file)
                shutil.move(source_path, destination_path)

    print("PDFs organized within their respective subfolders.")

# Define the main directory to start organizing PDFs
folder = r'D:\GRID\NGA\map_production\NGA_Gombe-Ogun_202402\output\20240308_jigawa_microplanning_300dpi'
organize_pdfs_in_subfolders(folder)
