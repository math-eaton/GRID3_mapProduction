import arcpy
from arcpy import env
import re

# Set environment settings
env.workspace = r"E:\mheaton\cartography\COD_KasaiOriental_microplanning_20240820\data\input\GRID3_COD_KO_consolidated_20240711.gdb"
env.overwriteOutput = True

# Set the local variables
joinFeatures = "GRID3_COD_KO_Health_areas_consolidation_20240711"
admin_fields = ["province", "zonesante", "airesante"]
pagename_fields = ["pagename_admin1", "pagename_admin2", "pagename_admin3"]

# Optional processing flags
perform_spatial_join = True  # Set this to False to skip pageName join to point fcs
perform_dissolve = True  # Set this to False to skip output admin dissolve post-process

# Ensure the fields do not already exist to prevent an error
existing_fields = [f.name for f in arcpy.ListFields(joinFeatures)]
for pagename_field in pagename_fields:
    if pagename_field not in existing_fields:
        arcpy.AddField_management(joinFeatures, pagename_field, "TEXT")

# Create pagename fields for each administrative level
arcpy.CalculateField_management(joinFeatures, pagename_fields[0], "'RDC_' + !{}!".format(admin_fields[0]), "PYTHON3")
arcpy.CalculateField_management(joinFeatures, pagename_fields[1], "'RDC_' + !{}! + '_' + !{}!".format(admin_fields[0], admin_fields[1]), "PYTHON3")
arcpy.CalculateField_management(joinFeatures, pagename_fields[2], "'RDC_' + !{}! + '_' + !{}! + '_' + !{}!".format(admin_fields[0], admin_fields[1], admin_fields[2]), "PYTHON3")

# Define a function to remove non-ascii characters and replace spaces, hyphens, slashes, and other problematic characters
code_block = """
def remove_non_ascii(text):
    # Remove non-ascii characters and replace spaces with hyphens
    cleaned_text = ''.join(i for i in text if ord(i)<128).replace(' ', '-')
    # Replace forward/backslashes, apostrophes, and ensure triple hyphens are reduced to single
    cleaned_text = re.sub('[\\\\/:*?"<>|]', '-', cleaned_text)
    cleaned_text = cleaned_text.replace('---', '-')
    return cleaned_text
"""

# Apply the function to the 'pagename' fields
for pagename_field in pagename_fields:
    arcpy.CalculateField_management(joinFeatures, pagename_field, "remove_non_ascii(!{}!)".format(pagename_field), "PYTHON3", code_block)

# Optional: Perform spatial join to point feature classes
if perform_spatial_join:
    # Get a list of only point feature classes in the gdb
    featureclasses = arcpy.ListFeatureClasses(feature_type="Point")

    # Loop through each feature class
    for targetFeatures in featureclasses:
        # Exclude the original joinFeatures from the loop
        if targetFeatures != joinFeatures:
            outfc = f"{targetFeatures}_pagename"

            # Use the Spatial Join tool to join the point feature class with the polygon feature class
            arcpy.analysis.SpatialJoin(targetFeatures, joinFeatures, outfc, join_type="KEEP_COMMON")

# Optional post-processing: Dissolve each pagename_[admin] into a new output feature class
if perform_dissolve:
    for pagename_field in pagename_fields:
        dissolve_output = f"{joinFeatures}_{pagename_field}_dissolved"

        # Perform the dissolve operation
        arcpy.management.Dissolve(joinFeatures, dissolve_output, pagename_field, multi_part="SINGLE_PART")

        # Check if the dissolve was successful and the output exists
        if arcpy.Exists(dissolve_output):
            print(f"Dissolved output created: {dissolve_output}")
        else:
            print(f"Failed to create dissolved output: {dissolve_output}")

print("done.")
