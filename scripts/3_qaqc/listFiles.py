import os
import pandas as pd

def list_files_to_excel(directories, output_excel, column_names=None):
    """
    List all individual file names from the specified directories and save them into an Excel spreadsheet.

    :param directories: List of directories to scan for files.
    :param output_excel: Path to the output Excel file.
    :param column_names: List of column names for each directory. If None, defaults to 'Directory 1', 'Directory 2', etc.
    """
    data = {}
    
    if column_names is None:
        column_names = [f"Directory {i + 1}" for i in range(len(directories))]
    
    for dir_path, col_name in zip(directories, column_names):
        try:
            files = os.listdir(dir_path)
            # Filter to include only files
            files = [f for f in files if os.path.isfile(os.path.join(dir_path, f))]
            data[col_name] = files
        except Exception as e:
            print(f"Error reading directory '{dir_path}': {e}")
            data[col_name] = []  # Leave the column empty if an error occurs
    
    # Find the maximum number of rows needed
    max_rows = max(len(col) for col in data.values())
    
    # Pad columns with empty strings to make them equal in length
    for col_name in data:
        data[col_name].extend([''] * (max_rows - len(data[col_name])))
    
    # Create a DataFrame and write to Excel
    df = pd.DataFrame(data)
    df.to_excel(output_excel, index=False)
    print(f"File names written to {output_excel}")

# Example usage
directories = [
    r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\OUTPUT_A2_microplanification_20241213_rename",
    r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\OUTPUT_A2_reference_20241215_Copy"
]
output_excel = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\file_names.xlsx"
list_files_to_excel(directories, output_excel)
