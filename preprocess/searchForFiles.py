import arcpy
import os

# List of directories to search
input_directories = ["D:\outputs\cod\MG", "D:\outputs\cod\MN\pre_alpha", "D:\outputs\cod\TP"]  # Update with your directories
text_fragments = ["settl", "facilit", "settl", "health", "htlfac"]  # Text fragments to search for
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

# Walk through each directory and search for feature classes and shapefiles
for directory in input_directories:
    arcpy.env.workspace = directory
    for dirpath, dirnames, filenames in arcpy.da.Walk():
        for filename in filenames:
            if contains_fragment(filename, text_fragments):
                full_path = os.path.join(dirpath, filename)
                desc = arcpy.Describe(full_path)

                # Check if the file is a shapefile or a feature class
                if desc.dataType in ["ShapeFile", "FeatureClass"]:
                    if filename.lower().endswith(".shp"):
                        # Define output path for shapefile
                        output_path = os.path.join(output_folder, filename)
                        if not os.path.exists(output_path):
                            arcpy.CopyFeatures_management(full_path, output_path)
                            print(f"Copied shapefile: {output_path}")
                        else:
                            print(f"Shapefile already exists, not copied: {output_path}")
                    else:
                        # Define output path for feature class
                        output_path = os.path.join(output_geodatabase, os.path.splitext(filename)[0])  # Remove file extension
                        if not arcpy.Exists(output_path):
                            arcpy.CopyFeatures_management(full_path, output_path)
                            print(f"Copied feature class: {output_path}")
                        else:
                            print(f"Feature class already exists, not copied: {output_path}")
                else:
                    print(f"Skipped non-feature class/table file: {full_path}")

print("Script completed.")
