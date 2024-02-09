import arcpy
import datetime
import os

arcpy.env.overwriteOutput = True

# Get current date in YYYYMMDD format
current_date = datetime.datetime.now().strftime("_%Y%m%d")

# Set your workspace and input feature class
arcpy.env.workspace = r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\processing\scratch_SK_KC.gdb"
input_feature_class = "SK_KC_zs_Merge"

# Output feature class to store exploded polygons
output_feature_class = input_feature_class + "_exploded" + current_date

# Create a spatial reference object
spatial_ref = arcpy.Describe(input_feature_class).spatialReference

# Create a field to store pageCount
arcpy.AddField_management(input_feature_class, "pageCount", "LONG")

# Start an edit session
edit = arcpy.da.Editor(arcpy.env.workspace)
edit.startEditing(False, True)

# Start an edit operation
edit.startOperation()

# Loop through the input feature class and set pageCount to 1 for singlepart polygons
with arcpy.da.UpdateCursor(input_feature_class, ["OID@", "SHAPE@", "pageCount"]) as cursor:
    for row in cursor:
        oid, shape, pageCount_field = row
        if shape.isMultipart:
            # Leave pageCount as None for multipart polygons to be handled later
            pageCount_field = None
        else:
            pageCount_field = 1
        row[2] = pageCount_field
        cursor.updateRow(row)

# Stop the edit operation and edit session
edit.stopOperation()
edit.stopEditing(True)

# Explode multipart polygons
arcpy.management.MultipartToSinglepart(input_feature_class, output_feature_class)

# Dictionary to store pageCount for each original OID
page_count_dict = {}

# Initialize a dictionary to store the area of each exploded part
exploded_parts_area = {}

# Iterate over the exploded polygons to calculate their area and update pageCount
with arcpy.da.UpdateCursor(output_feature_class, ["OID@", "ORIG_FID", "SHAPE@AREA", "pageCount"]) as cursor:
    for row in cursor:
        oid, orig_fid, area, page_count_field = row
        exploded_parts_area[oid] = area  # Store area of each part
        if orig_fid not in page_count_dict:
            page_count_dict[orig_fid] = 1
        else:
            page_count_dict[orig_fid] += 1
        page_count_field = page_count_dict[orig_fid]
        row[3] = page_count_field
        cursor.updateRow(row)

# Update the original feature class with the correct pageCount for multipart polygons
with arcpy.da.UpdateCursor(input_feature_class, ["OID@", "pageCount"]) as cursor:
    for row in cursor:
        oid, pageCount_field = row
        if oid in page_count_dict:
            pageCount_field = page_count_dict[oid]
        row[1] = pageCount_field
        cursor.updateRow(row)

# Generate a combined report of multipart polygons, their areas of exploded parts
# Use input feature class name in the report file name
report_file_name = input_feature_class + current_date + ".txt"
report_file_path = os.path.join(r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\processing", report_file_name)

with open(report_file_path, "w") as report_file:
    report_file.write("FID,Area\n")
    for oid, area in exploded_parts_area.items():
        report_file.write(f"{oid},{area}\n")

print("done")
