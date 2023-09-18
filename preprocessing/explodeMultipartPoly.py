import arcpy

# Set your workspace and input feature class
arcpy.env.workspace = r"C:\Path\to\Your\Workspace"
input_feature_class = "YourInputFeatureClass"

# Output feature class to store exploded polygons
output_feature_class = "ExplodedPolygons"

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
                if distance > 5000:  # Check if distance is greater than 5km
                    cursor.deleteRow()
            pageCount_field = 1  # Set pageCount to 1 for exploded parts
        else:
            pageCount_field = page_count
            page_count += 1
        row[2] = pageCount_field
        cursor.updateRow(row)

# Stop the edit operation and edit session
edit.stopOperation()
edit.stopEditing(True)

# Generate a report of multipart polygons and their distances
report_file = open("MultipartReport.txt", "w")
report_file.write("FID,Distance\n")
for oid, distance in distance_list:
    report_file.write(f"{oid},{distance}\n")
report_file.close()

# Explode multipart polygons
arcpy.management.MultipartToSinglepart(input_feature_class, output_feature_class)

print("Script completed successfully!")
