import arcpy
import os
import datetime

def sanitize_name(name):
    """ Sanitize names to be ASCII-compliant and suitable for filenames """
    sanitized = ''.join(c if c.isalnum() else '_' for c in name)
    return sanitized

def copy_geodatabase_contents(input_folder, output_gdb):
    """ Copy all geodatabase contents from subfolders into a consolidated geodatabase """
    arcpy.env.overwriteOutput = True

    # Gather today's date in the specified format
    today_str = datetime.datetime.now().strftime("_%Y%m%d")

    # Walk through the directory
    for dirpath, dirnames, filenames in os.walk(input_folder):
        for dirname in dirnames:
            # Check if the directory is a geodatabase
            if dirname.endswith(".gdb"):
                gdb_path = os.path.join(dirpath, dirname)
                arcpy.env.workspace = gdb_path

                # List all feature classes, including those within feature datasets
                for dataset in arcpy.ListDatasets() + ['']:
                    for feature_class in arcpy.ListFeatureClasses(feature_dataset=dataset):
                        # Construct the output path with sanitized names and append the current date
                        new_name = sanitize_name(feature_class) + today_str
                        out_feature_class = os.path.join(output_gdb, new_name)
                        arcpy.CopyFeatures_management(feature_class, out_feature_class)
                        print(f"Copied {feature_class} to {out_feature_class}")

                # List all tables and copy them
                for table in arcpy.ListTables():
                    new_name = sanitize_name(table) + today_str
                    out_table = os.path.join(output_gdb, new_name)
                    arcpy.TableToTable_conversion(table, output_gdb, new_name)
                    print(f"Copied {table} to {out_table}")

if __name__ == "__main__":
    input_folder = r'E:\mheaton\cartography\COD_microplanning_042024\data\input'  # Path to the input folder
    output_gdb = r'E:\mheaton\cartography\COD_microplanning_042024\data\consolidated\consolidated.gdb'  # Path to the output consolidated geodatabase

    # Ensure the output geodatabase exists
    if not arcpy.Exists(output_gdb):
        arcpy.CreateFileGDB_management(os.path.dirname(output_gdb), os.path.basename(output_gdb))
        print(f"Created geodatabase at {output_gdb}")

    copy_geodatabase_contents(input_folder, output_gdb)
