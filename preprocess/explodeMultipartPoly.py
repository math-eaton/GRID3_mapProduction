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

# Check for multipart polygons
multipart_exists = False
with arcpy.da.SearchCursor(input_feature_class, ["SHAPE@"]) as cursor:
    for row in cursor:
        if row[0].isMultipart:
            multipart_exists = True
            break

# Proceed only if multipart polygons exist
if multipart_exists:
    # Create a field to store pageCount
    arcpy.AddField_management(input_feature_class, "pageCount", "LONG")

    # Explode multipart polygons
    arcpy.management.MultipartToSinglepart(input_feature_class, output_feature_class)

    # Initialize a dictionary to store the area of each exploded part
    exploded_parts_area = {}

    # Iterate over the exploded polygons to calculate their area
    with arcpy.da.SearchCursor(output_feature_class, ["OID@", "SHAPE@AREA"]) as cursor:
        for row in cursor:
            oid, area = row
            exploded_parts_area[oid] = area

    # Generate a report file only if there are exploded parts
    if exploded_parts_area:
        report_file_name = input_feature_class + current_date + ".txt"
        report_file_path = os.path.join(r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\processing", report_file_name)

        with open(report_file_path, "w") as report_file:
            report_file.write("FID,Area\n")
            for oid, area in exploded_parts_area.items():
                report_file.write(f"{oid},{area}\n")
else:
    print("No multipart polygons in input")

print("done")
