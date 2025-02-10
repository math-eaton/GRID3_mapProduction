import arcpy
from arcpy import env

# todo add alternative pagenames for different admin level uids in case

# Set environment settings
env.workspace = r"E:\mheaton\cartography\COD_microplanning_042024\data\consolidated\consolidated.gdb"
env.overwriteOutput = True

# Set the local variables
joinFeatures = "GRID3_COD_MN_health_areas_v1_0_20240430"
indexField = "pageName" 

# Ensure the field does not already exist to prevent an error
fields = [f.name for f in arcpy.ListFields(joinFeatures)]
if indexField not in fields:
    arcpy.AddField_management(joinFeatures, indexField, "TEXT")

# Concatenate 'admin1', 'admin2', and 'admin3' fields with an underscore separator
# arcpy.CalculateField_management(joinFeatures, indexField, "'RDC_' + !province! + '_' + !zonesante! + '_' + !airesante!", "PYTHON3")
arcpy.CalculateField_management(joinFeatures, indexField, "'NGA_OG_' + !LGA! + '_' + !WARD!", "PYTHON3")

# Define a consolidated function to clean up the text
code_block = """
def clean_text(text):
    # Remove non-ascii characters and replace spaces with hyphens
    cleaned_text = ''.join(i for i in text if ord(i)<128).replace(' ', '-')
    # Replace forward/backslashes, apostrophes, and ensure triple hyphens are reduced to single
    cleaned_text = cleaned_text.replace('/', '-').replace('\\\\', '-').replace("'", '')
    return cleaned_text.replace('---', '-')
"""

# Apply the consolidated function to clean up the indexField
arcpy.CalculateField_management(joinFeatures, indexField, "clean_text(!{}!)".format(indexField), "PYTHON3", code_block)

print("done.")