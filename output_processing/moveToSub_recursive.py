import os
import shutil

def organize_pdfs(folder):
    # Flag to check if any PDFs have been organized
    pdfs_organized = False

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
                    target = pdf_file.split('_')[4]
                except IndexError:
                    # Handle case where filename does not contain enough parts to split
                    print(f"Skipping {pdf_file}: cannot extract target folder from filename")
                    continue

                # Create the target directory if it doesn't exist
                target_directory = os.path.join(folder, target)
                if not os.path.exists(target_directory):
                    os.makedirs(target_directory)

                # Move the PDF file to the target directory
                source_path = os.path.join(root, pdf_file)
                destination_path = os.path.join(target_directory, pdf_file)
                shutil.move(source_path, destination_path)
                pdfs_organized = True

    if pdfs_organized:
        print("PDFs organized.")
    else:
        print("No PDFs found to organize.")

folder = r'D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\output\20240202'
organize_pdfs(folder)
