import os
import csv
import glob
from datetime import datetime

# Configuration
input_file = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\HK_Mapindex_ExportTable_20241214.csv"  # or .xlsx if needed
output_directory = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\OUTPUT_A2_microplanification_20241213_rename"
missing_report = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\missing.txt"
use_case = "microplanification"
layout_size = "A2"
date_str = datetime.now().strftime('%Y%m%d')  # or a fixed date "20241214"

# If you have an XLSX file instead of CSV:
# import openpyxl
# workbook = openpyxl.load_workbook(input_file)
# sheet = workbook.active
# rows = sheet.iter_rows(values_only=True)
# header = next(rows)
# index_of_interest = header.index('pagename_airesante')

# For CSV reading
with open(input_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    input_names = [row['pagename_airesante'] for row in reader]

def transform_input_name(name):
    """
    Transform the input name (e.g. "RDC_Haut-Katanga_Likasi_Kambove_Dikula")
    into the output pattern:
    A2_RDC_HAUT-KATANGA_LIKASI_KAMBOVE_DIKULA_microplanification_YYYYMMDD

    Adjust this logic to match your exact output formatting rules.
    """
    parts = name.split("_")
    # Expected structure: RDC, Haut-Katanga, Likasi, Kambove, Dikula
    # Convert them to uppercase (except RDC might already be uppercase)
    # and follow the output naming pattern.
    parts = [p.upper() for p in parts]

    # Insert the A2 prefix, then join everything with underscores
    # Pattern: A2_RDC_HAUT-KATANGA_LIKASI_KAMBOVE_DIKULA_microplanification_YYYYMMDD
    transformed = f"{layout_size}_{'_'.join(parts)}_{use_case}_{date_str}"
    return transformed

missing_entries = []

for input_name in input_names:
    # Transform the input name to the expected output basename
    base_output = transform_input_name(input_name)
    # The files in output are JPEG with possible duplicates as:
    # base_output.jpg or base_output_1.jpg, base_output_2.jpg, etc.
    # Use glob to check if any file matches this pattern
    pattern = os.path.join(output_directory, base_output + "*.jpg")
    matches = glob.glob(pattern)

    if not matches:
        # No file found for this input name
        missing_entries.append(input_name)

# Write missing entries to a report
if missing_entries:
    with open(missing_report, 'w', encoding='utf-8') as f:
        for entry in missing_entries:
            f.write(entry + "\n")
    print(f"Missing entries report written to {missing_report}")
else:
    print("No missing entries. All input names have corresponding output files.")
