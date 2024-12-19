import os
import shutil
import argparse
import zipfile

def organize_files_in_nested_subfolders(folder, start_index, end_index, file_extension=".jpg", zip_folders=False):
    """
    Organizes files into nested subfolders based on filename indices between start_index and end_index.
    :param folder: Top-level directory to start organizing.
    :param start_index: Starting index for creating subdirectories.
    :param end_index: Ending index for creating subdirectories.
    :param file_extension: File extension to filter for organizing.
    :param zip_folders: Whether to create compressed zip archives for each top-level folder.
    """
    created_top_folders = set()  # Track created top-level folders for zipping

    # Walk through all folders and subfolders
    for root, dirs, files in os.walk(folder):
        # Filter for the specified file type
        target_files = [file for file in files if file.lower().endswith(file_extension)]
        
        if target_files:
            for target_file in target_files:
                # Split the filename into parts
                parts = target_file.split('_')
                
                try:
                    # Construct the nested folder path
                    nested_path_parts = parts[start_index:end_index + 1]
                    if not nested_path_parts:
                        raise IndexError(f"Filename '{target_file}' does not have enough parts for the specified indices.")
                    
                    nested_folder_path = os.path.join(root, *nested_path_parts)
                    
                    # Create the nested directory structure
                    if not os.path.exists(nested_folder_path):
                        os.makedirs(nested_folder_path)
                    
                    # Add the top-level folder to the tracking set
                    top_folder = os.path.join(root, parts[start_index])
                    created_top_folders.add(top_folder)
                    
                    # Move the file into the deepest folder in the nested structure
                    source_path = os.path.join(root, target_file)
                    destination_path = os.path.join(nested_folder_path, target_file)
                    shutil.move(source_path, destination_path)
                except IndexError:
                    print(f"Skipping {target_file}: cannot extract indices between {start_index} and {end_index}")
                    continue

    # Optionally create zip archives for top-level folders
    if zip_folders:
        for folder_to_zip in created_top_folders:
            zip_file_path = f"{folder_to_zip}.zip"
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(folder_to_zip):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=folder_to_zip)
                        zipf.write(file_path, arcname)
            print(f"Compressed {folder_to_zip} into {zip_file_path}")

    print("Files organized into nested subfolders and optionally zipped.")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Organize files into nested subdirectories based on filename indices and optionally compress top-level subfolders.")
    parser.add_argument("folder", help="Top-level directory to organize files.")
    parser.add_argument(
        "--file_extension", type=str, default=".jpg", 
        help="File extension to filter for organizing (default is .jpg)."
    )
    parser.add_argument(
        "--zip_folders", action="store_true", 
        help="Create zip archives of each top-level folder created at the start index level."
    )

    args = parser.parse_args()

    # Display a sample filename to help the user decide split indices
    try:
        sample_files = [f for f in os.listdir(args.folder) if f.lower().endswith(args.file_extension)]
        if sample_files:
            print(f"Sample filename: {sample_files[0]}")
            print("Examine the sample filename to determine the appropriate start and end indices.")
        else:
            print(f"No files with extension '{args.file_extension}' found in the directory.")
            exit(1)
    except Exception as e:
        print(f"Error reading directory: {e}")
        exit(1)

    # Pause and ask user for start and end indices interactively
    start_index = int(input("Enter the start index for splitting (e.g., 0): "))
    end_index = int(input("Enter the end index for splitting (inclusive, e.g., 4): "))

    # Call the function with user-specified indices
    organize_files_in_nested_subfolders(
        folder=args.folder, 
        start_index=start_index, 
        end_index=end_index, 
        file_extension=args.file_extension, 
        zip_folders=args.zip_folders
    )
