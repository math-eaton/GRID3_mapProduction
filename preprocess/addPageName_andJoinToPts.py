import arcpy
from arcpy import env
import re

# Set environment settings
env.workspace = r"E:\mheaton\cartography\NGA_microplanning_2024\data\processing\Ogun_NMEP_maps_layers_processing.gdb"
env.overwriteOutput = True

# Set the local variables
joinFeatures = "GRID3_NGA_Ogun_wards_ek_20240328"
indexField = "pagename"

# Ensure the field does not already exist to prevent an error
fields = [f.name for f in arcpy.ListFields(joinFeatures)]
if indexField not in fields:
    arcpy.AddField_management(joinFeatures, indexField, "TEXT")

# Concatenate 'admin1', 'admin2', and 'admin3' fields with an underscore separator
# Ensure field names are correctly referenced
arcpy.CalculateField_management(joinFeatures, indexField, "'RDC_' + !province! + '_' + !zonesante! + '_' + !airesante!", "PYTHON3")

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

# Apply the function to the 'pagename' field
arcpy.CalculateField_management(joinFeatures, indexField, "remove_non_ascii(!{}!)".format(indexField), "PYTHON3", code_block)

# Get a list of only point feature classes in the gdb
featureclasses = arcpy.ListFeatureClasses(feature_type="Point")

# Loop through each feature class
for targetFeatures in featureclasses:
    # Exclude the original joinFeatures from the loop
    if targetFeatures != joinFeatures:
        outfc = f"{targetFeatures}_pagename"

        # Use the Spatial Join tool to join the two feature classes.
        arcpy.analysis.SpatialJoin(targetFeatures, joinFeatures, outfc)

print("done.")
