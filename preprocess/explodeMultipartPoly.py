import arcpy
import datetime
import os

# Get current date in YYYYMMDD format
current_date = datetime.datetime.now().strftime("_%Y%m%d")

# Set your workspace and input feature class
arcpy.env.workspace = r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\raw\COD_raw_MN_MG_TS_2024.gdb"
input_feature_class = "GRID3_COD_TP_health_areas_ek_20231215"
arcpy.env.overwriteOutput = True

# Output feature class to store exploded polygons
output_feature_class = input_feature_class + "_exploded_" + current_date

# Create a spatial reference object
spatial_ref = arcpy.Describe(input_feature_class).spatialReference

# Create a list to store the FIDs of multipart polygons
multipart_fid_list = []

# Create a list to store the calculated distances between parts
distance_list = []

# Create a dictionary to store polygon counts
polygon_count_dict = {}

# Create a field to store pageCount
arcpy.AddField_management(input_feature_class, "pageCount", "LONG")

# Initialize a pageCount counter
page_count = 1

# Start an edit session
edit = arcpy.da.Editor(arcpy.env.workspace)
edit.startEditing(False, True)

# Start an edit operation
edit.startOperation()

# Loop through the input feature class
with arcpy.da.UpdateCursor(input_feature_class, ["OID@", "SHAPE@", "pageCount"]) as cursor:
    for row in cursor:
        oid, shape, pageCount_field = row
        if shape.isMultipart:
            multipart_fid_list.append(oid)
            multipart = shape
            for part in multipart:
                part_geometry = arcpy.Polygon(part, spatial_ref)
                distance = part_geometry.distanceTo(multipart)
                distance_list.append((oid, distance))
            pageCount_field = 1  # Set pageCount to 1 for exploded parts
        else:
            pageCount_field = page_count
            page_count += 1
        row[2] = pageCount_field
        cursor.updateRow(row)

# Stop the edit operation and edit session
edit.stopOperation()
edit.stopEditing(True)

# Explode multipart polygons
arcpy.management.MultipartToSinglepart(input_feature_class, output_feature_class)

# Initialize a dictionary to store the area of each exploded part
exploded_parts_area = {}

# Iterate over the exploded polygons to calculate their area
with arcpy.da.SearchCursor(output_feature_class, ["OID@", "SHAPE@AREA"]) as cursor:
    for row in cursor:
        oid, area = row
        exploded_parts_area[oid] = area

# Generate a combined report of multipart polygons, their distances, and areas of exploded parts
# Use input feature class name in the report file name
report_file_name = input_feature_class + current_date + ".txt"
report_file_path = os.path.join(r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\processing", report_file_name)

with open(report_file_path, "w") as report_file:
    report_file.write("FID,Distance,Area\n")
    for oid, distance in distance_list:
        area = exploded_parts_area.get(oid, "N/A")
        report_file.write(f"{oid},{distance},{area}\n")

print("done")
