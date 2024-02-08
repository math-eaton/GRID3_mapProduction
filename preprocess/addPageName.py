import arcpy
from arcpy import env

# Set environment settings
env.workspace = r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\processing\boundaries.gdb"
env.overwriteOutput = True

# Set the local variables
joinFeatures = "TP_MG_aire_sante"
join_field = "pagename"

# Ensure the field does not already exist to prevent an error
fields = [f.name for f in arcpy.ListFields(joinFeatures)]
if join_field not in fields:
    arcpy.AddField_management(joinFeatures, join_field, "TEXT")

# Concatenate 'admin1', 'admin2', and 'admin3' fields with an underscore separator
arcpy.CalculateField_management(joinFeatures, join_field, "'RDC_' + !province! + '_' + !zone_sante! + '_' + !aire_sante!", "PYTHON3")

# Define a function to remove non-ascii characters and replace spaces with hyphens
code_block = """
def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128).replace(' ', '-')
"""

# Apply the function to the 'pagename' field
arcpy.CalculateField_management(joinFeatures, join_field, "remove_non_ascii(!{}!)".format(join_field), "PYTHON3", code_block)

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