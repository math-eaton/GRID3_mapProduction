import arcpy
import csv

# Set the workspace and feature class
arcpy.env.workspace = "path_to_your_gdb"
feature_class = "your_osm_roads_feature_class"
csv_file = "path_to_your_csv_file"  # Update this to the path of your CSV file

# Add the new field for simplified fclass categories
arcpy.AddField_management(feature_class, "fclass_simplified", "TEXT")

# Create a dictionary for fclass simplification from the CSV file
fclass_simplified_dict = {}

with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        for category, fclass in row.items():
            if fclass:
                fclass_simplified_dict[fclass] = category

# Update the fclass_simplified field based on the fclass field
with arcpy.da.UpdateCursor(feature_class, ["fclass", "fclass_simplified"]) as cursor:
    for row in cursor:
        fclass_value = row[0]
        row[1] = fclass_simplified_dict.get(fclass_value, "Other")  # Default to "Other" if fclass not found
        cursor.updateRow(row)

print("fclass_simplified field updated successfully.")
