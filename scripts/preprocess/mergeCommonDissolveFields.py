# Purpose: 
# to merge polygon, point, or line feature classes within a geodatabase
# that contain common admin level keywords

import arcpy
from arcpy import env
import os

# Set environment settings and input/output geodatabases
env.workspace = r"E:\mheaton\cartography\COD_PEV_smallScale_overviews_20241007\data\processing.gdb"
target_gdb = r"E:\mheaton\cartography\COD_PEV_smallScale_overviews_20241007\data\merged.gdb"

# Overwrite outputs
env.overwriteOutput = True

# Define the admin dissolve fields (also serve as text to match in feature class names)
admin_fields = ["province", "antenne", "zonesante", "airesante"]

# Function to list feature classes with the same geometry type and containing admin field in their name
def find_matching_feature_classes_by_admin(geometry_type, admin_field):
    matching_fcs = []
    
    # Get all feature classes in the workspace
    featureclasses = arcpy.ListFeatureClasses()
    
    for fc in featureclasses:
        desc = arcpy.Describe(fc)
        
        # Check if the geometry matches and if the admin field is part of the name
        if desc.shapeType == geometry_type and admin_field in fc:
            matching_fcs.append(fc)
    
    return matching_fcs

# Function to merge feature classes with the same geometry and admin field
def merge_feature_classes_by_admin(matching_fcs, geometry_type, admin_field):
    if matching_fcs:
        print(f"Merging feature classes: {matching_fcs}")
        
        # Define the output feature class name
        output_fc_name = f"merged_{geometry_type.lower()}_{admin_field}_dissolved"
        
        # Perform merge operation
        merged_output = os.path.join(target_gdb, output_fc_name)
        
        # Check if the output already exists and delete it if necessary
        if arcpy.Exists(merged_output):
            arcpy.management.Delete(merged_output)
            print(f"Existing output deleted: {merged_output}")
        
        print(f"Attempting to create output at: {merged_output}")
        arcpy.management.Merge(matching_fcs, merged_output)
        
        # Check if the merge was successful
        if arcpy.Exists(merged_output):
            print(f"Feature classes merged successfully: {merged_output}")
        else:
            print(f"Failed to merge feature classes: {matching_fcs}")
    else:
        print(f"No matching feature classes found for admin field: {admin_field}")

# Main processing block
def main():
    # Define geometry types to search for (Polygon, Point, Polyline)
    geometry_types = ["Polygon", "Point", "Polyline"]
    
    # Loop through each geometry type
    for geometry_type in geometry_types:
        print(f"Processing geometry type: {geometry_type}")
        
        # Loop through each admin field
        for admin_field in admin_fields:
            print(f"Searching for feature classes with admin field in name: {admin_field}")
            
            # Find feature classes with matching geometry and the specific admin field in their name
            matching_fcs = find_matching_feature_classes_by_admin(geometry_type, admin_field)
            
            if matching_fcs:
                # Merge the feature classes that share the same geometry type and admin field
                merge_feature_classes_by_admin(matching_fcs, geometry_type, admin_field)
            else:
                print(f"No matching feature classes found for geometry type: {geometry_type} and admin field: {admin_field}")

# Run the main function
if __name__ == "__main__":
    main()

print("Processing complete.")
