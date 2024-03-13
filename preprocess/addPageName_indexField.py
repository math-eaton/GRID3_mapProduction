import arcpy
from arcpy import env

# Set environment settings
env.workspace = r"D:\GRID\NGA\map_production\NGA_Gombe-Ogun_202402\data\raw\NGA_202402_consolidated.gdb"
env.overwriteOutput = True

# Set the local variables
joinFeatures = "gombe_ward_bry_wPop_20240313"
indexField = "pageName" 

# Ensure the field does not already exist to prevent an error
fields = [f.name for f in arcpy.ListFields(joinFeatures)]
if indexField not in fields:
    arcpy.AddField_management(joinFeatures, indexField, "TEXT")

# Concatenate 'admin1', 'admin2', and 'admin3' fields with an underscore separator
arcpy.CalculateField_management(joinFeatures, indexField, "'NGA_' + !statename! + '_' + !lganame! + '_' + !wardname!", "PYTHON3")

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