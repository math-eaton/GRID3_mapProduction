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

# Get a list of only point feature classes in the gdb
featureclasses = arcpy.ListFeatureClasses(feature_type="Point")

# Loop through each feature class
for targetFeatures in featureclasses:
    # Exclude the original joinFeatures from the loop
    if targetFeatures != joinFeatures:
        for pagename_field in pagename_fields:
            outfc = f"{targetFeatures}_{pagename_field}"

            # Use the Spatial Join tool to join the two feature classes.
            arcpy.analysis.SpatialJoin(targetFeatures, joinFeatures, outfc)

print("done.")
