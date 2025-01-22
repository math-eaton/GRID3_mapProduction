import os
import pandas as pd
import fnmatch

def find_spreadsheets_with_microplan(root_dir):
    matches = []
    for root, dirnames, filenames in os.walk(root_dir):
        for filename in fnmatch.filter(filenames, '*microplan*.xlsx'):
            matches.append(os.path.join(root, filename))
    return matches

def best_matching_sheet_name(sheet_names, target_name):
    best_match = None
    best_score = 0
    for name in sheet_names:
        score = sum(c in target_name for c in name.lower())
        if score > best_score:
            best_score = score
            best_match = name
    return best_match

def extract_health_facility_headers(file_paths):
    headers_list = []
    for file_path in file_paths:
        try:
            # Load all sheet names to find the best match
            xls = pd.ExcelFile(file_path)
            matched_sheet_name = best_matching_sheet_name(xls.sheet_names, 'health facilities')
            
            if matched_sheet_name:
                df = pd.read_excel(file_path, sheet_name=matched_sheet_name)
                headers = [header for header in df.columns if 'health facility' in header.lower()]
                headers_list.append(','.join(headers))
            else:
                print(f"No matching sheet found in file {file_path}")

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    return headers_list

# Example usage
root_directory = '/path/to/your/directory'  # Replace with your directory path
spreadsheet_files = find_spreadsheets_with_microplan(root_directory)
extracted_headers = extract_health_facility_headers(spreadsheet_files)
for headers in extracted_headers:
    print(headers)
