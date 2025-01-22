import arcpy
import os

# Define the input geodatabase and the search string
input_gdb = r'E:\mheaton\data_processing\NGA_Ogun_P3B_match_20240921\data\output_round2\output_dp_walk\output.gdb'  # Update this path
search_string = "catchments_dp"
output_merged_fc = r'E:\mheaton\data_processing\NGA_Ogun_P3B_match_20240921\data\output_round2\output_dp_walk\merged_FC.gdb\mergedCatchmentsDP'  # Update the output feature class path

# Set the workspace to the input geodatabase
arcpy.env.workspace = input_gdb

# List all feature classes in the geodatabase
feature_classes = arcpy.ListFeatureClasses()

# Create a list to store feature classes that match the search string
matching_feature_classes = []

# Loop through all feature classes and find the ones that contain the search string
for fc in feature_classes:
    if search_string in fc:
        # Check if the feature class is of polygon geometry type
        desc = arcpy.Describe(fc)
        if desc.shapeType == "Polygon":
            matching_feature_classes.append(fc)

# Merge the matching feature classes
if matching_feature_classes:
    arcpy.Merge_management(matching_feature_classes, output_merged_fc)
    print(f"Merged feature classes: {matching_feature_classes} into {output_merged_fc}")
else:
    print(f"No feature classes found with the text '{search_string}' in the geodatabase.")
