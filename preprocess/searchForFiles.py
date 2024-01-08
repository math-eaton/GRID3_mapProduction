import arcpy
import os
import datetime
import re


# List of directories to search
input_directories = ["D:\outputs\cod\MG", "D:\outputs\cod\MN\pre_alpha", "D:\outputs\cod\TP"]  # Update with your directories
text_fragments = ["settl", "facilit", "settl", "health", "hltfac"]  # Text fragments to search for
output_geodatabase = r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\raw\COD_raw_MN_MG_TS_2024.gdb"  # Update with your geodatabase path
output_folder = r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\raw\COD_raw_MN_MG_TS_2024"  # Update with your output folder path

arcpy.env.overwriteOutput = True

# Function to check if any of the text fragments are in the file name
def contains_fragment(filename, fragments):
    return any(fragment in filename for fragment in fragments)

# Check if output paths exist and are accessible
if not os.path.exists(output_geodatabase):
    print(f"Output geodatabase does not exist: {output_geodatabase}")
    exit(1)

if not os.path.exists(output_folder):
    print(f"Output folder does not exist: {output_folder}")
    exit(1)

def parse_date_from_filename(filename):
    """Extracts a date in YYYYMMDD format from the filename."""
    match = re.search(r'(\d{4})(\d{2})(\d{2})', filename)
    if match:
        return datetime.datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return None

def get_base_filename(filename):
    """Extracts the base filename by removing the date suffix."""
    return re.sub(r'\d{8}', '', filename)

# Initialize counters and lists for the report
copied_files = []
ignored_files = []
total_files = 0

# Dictionary to keep track of most recent files
most_recent_files = {}

# Walk through each directory and search for feature classes and shapefiles
for directory in input_directories:
    arcpy.env.workspace = directory
    for dirpath, dirnames, filenames in arcpy.da.Walk():
        for filename in filenames:
            total_files += 1
            if contains_fragment(filename, text_fragments):
                full_path = os.path.join(dirpath, filename)
                desc = arcpy.Describe(full_path)

                if desc.dataType in ["ShapeFile", "FeatureClass"]:
                    base_filename = get_base_filename(filename)
                    file_date = parse_date_from_filename(filename)

                    if base_filename not in most_recent_files or (file_date and most_recent_files[base_filename]['date'] < file_date):
                        most_recent_files[base_filename] = {'path': full_path, 'date': file_date}
                else:
                    ignored_files.append(filename)
                    print(f"Ignored (not a feature class or shapefile): {filename}")
            else:
                ignored_files.append(filename)
                print(f"Ignored (does not contain specified text fragment): {filename}")

# Now copy the most recent files and prepare the report
report_path = os.path.join(output_folder, "copy_report.txt")
with open(report_path, "w") as report_file:
    for base_filename, file_info in most_recent_files.items():
        full_path = file_info['path']
        filename = os.path.basename(full_path)

        if filename.lower().endswith(".shp"):
            output_path = os.path.join(output_folder, filename)
            if not os.path.exists(output_path):
                arcpy.CopyFeatures_management(full_path, output_path)
                copied_files.append(filename)
                print(f"Copied shapefile: {filename}")
        else:
            output_path = os.path.join(output_geodatabase, os.path.splitext(filename)[0])
            if not arcpy.Exists(output_path):
                arcpy.CopyFeatures_management(full_path, output_path)
                copied_files.append(filename)
                print(f"Copied feature class: {filename}")

    # Writing to report file
    report_file.write("Files Copied:\n")
    report_file.writelines("\n".join(copied_files) + "\n\n")
    
    report_file.write("Files Ignored:\n")
    report_file.writelines("\n".join(ignored_files) + "\n\n")

    # Summary
    report_file.write(f"Summary:\nTotal Files Processed: {total_files}\n")
    report_file.write(f"Total Files Copied: {len(copied_files)}\n")
    report_file.write(f"Total Files Ignored: {len(ignored_files)}\n")

print("Script completed. Report generated at:", report_path)
