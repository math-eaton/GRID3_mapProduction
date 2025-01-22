import os
import shutil

def copy_files_by_extension(source_dir, target_dir, file_extension):
    """
    Copies files with the specified extension from source_dir (including subdirectories) 
    to target_dir.
    
    Args:
        source_dir (str): The source directory to search for files.
        target_dir (str): The target directory where files will be copied.
        file_extension (str): The file extension to match (e.g., '.jpg', '.pdf').
    """
    if not os.path.exists(source_dir):
        print(f"Source directory does not exist: {source_dir}")
        return

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(file_extension.lower()):
                source_path = os.path.join(root, file)
                target_path = os.path.join(target_dir, file)
                
                # Ensure unique filenames in the target directory
                base, ext = os.path.splitext(file)
                counter = 1
                while os.path.exists(target_path):
                    target_path = os.path.join(target_dir, f"{base}_{counter}{ext}")
                    counter += 1
                
                shutil.copy2(source_path, target_path)
                print(f"Copied: {source_path} -> {target_path}")

if __name__ == "__main__":
    # Define the source directory, target directory, and file extension
    source_directory = input("Enter the source directory: ").strip()
    target_directory = input("Enter the target directory: ").strip()
    extension = input("Enter the file extension (e.g., '.jpg', '.pdf'): ").strip()

    copy_files_by_extension(source_directory, target_directory, extension)
