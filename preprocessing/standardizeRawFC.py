import arcpy
import os
from datetime import datetime

# Set up the workspace and geodatabase
workspace = r'C:\path\to\your\geodatabase'  # Replace with the path to your geodatabase
arcpy.env.workspace = workspace

# Define a dictionary to map old layer names to new names
name_mapping = {
    'OldLayer1': 'NewLayer1',
    'OldLayer2': 'NewLayer2',
    'OldLayer3': 'NewLayer3',
    # Add more mappings as needed
}

# Define a dictionary to map feature class types
fc_types = {
    'Point': 'point',
    'Polyline': 'line',
    'Polygon': 'polygon',
    # Add more types as needed
}

# Get the current date in YYYYMMDD format
current_date = datetime.now().strftime('%Y%m%d')

# Iterate through the feature classes in the geodatabase
for fc in arcpy.ListFeatureClasses():
    # Get the dataset and layer name without the path
    dataset, old_name = os.path.split(fc)

    # Check if the old layer name is in the mapping dictionary
    if old_name in name_mapping:
        new_name = name_mapping[old_name]

        # Get the feature class type
        desc = arcpy.Describe(fc)
        fc_type = fc_types.get(desc.dataType, 'unknown')

        # Construct the new name with the feature class type and date
        new_name = f"{new_name}_{fc_type}_{current_date}"

        # Rename the feature class
        arcpy.Rename_management(fc, os.path.join(dataset, new_name))
        print(f"Renamed '{old_name}' to '{new_name}'")

print("Script completed.")
