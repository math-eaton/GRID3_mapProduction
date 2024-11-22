import arcpy
from arcpy import env
import re



# Set environment settings
env.workspace = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\data\20241121\input\input.gdb"

# Set the target geodatabase for output feature classes
target_gdb = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\data\20241121\processed\processed.gdb"

env.overwriteOutput = True

# Set the local variables
joinFeatures = "merged_aireSante_20241121"
admin_fields = ["province", "antenne" ,"zonesante", "airesante"]

# Dynamically generate pagename fields based on admin_fields
pagename_fields = [f"pagename_{admin}" for admin in admin_fields]

# Optional processing flags
perform_spatial_join = True  # Set this to False if you don't want to perform the spatial join
perform_dissolve = True  # Set this to False if you don't want to perform the dissolve operation
perform_polygon_to_line = True  # Set this to False if you don't want to convert polygons to lines

# Ensure only the dynamically named fields are created
existing_fields = [f.name for f in arcpy.ListFields(joinFeatures)]
for pagename_field in pagename_fields:
    if pagename_field not in existing_fields:
        arcpy.AddField_management(joinFeatures, pagename_field, "TEXT")

# Create pagename fields for each administrative level
for i, pagename_field in enumerate(pagename_fields):
    if i == 0:
        expression = f"'RDC_' + !{admin_fields[i]}!"
    else:
        expression = "'RDC_' + " + " + '_' + ".join([f'!{admin_fields[j]}!' for j in range(i+1)])
    
    arcpy.CalculateField_management(joinFeatures, pagename_field, expression, "PYTHON3")

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
            outfc = f"{target_gdb}\\{targetFeatures}_pagename"

            # Use the Spatial Join tool to join the point feature class with the polygon feature class
            arcpy.analysis.SpatialJoin(targetFeatures, joinFeatures, outfc, join_type="KEEP_COMMON")

# Optional post-processing: Dissolve each pagename_[admin] into a new output feature class
if perform_dissolve:
    for i, pagename_field in enumerate(pagename_fields):
        dissolve_output = f"{target_gdb}\\{joinFeatures}_{pagename_field}_dissolved"
        
        # Preserve original admin fields in the dissolve
        dissolve_fields = [f"FIRST_{admin_fields[j]}" for j in range(i+1)]
        dissolve_stats = [[admin_fields[j], "FIRST"] for j in range(i+1)]

        # Perform the dissolve operation
        arcpy.management.Dissolve(joinFeatures, dissolve_output, pagename_field, dissolve_stats, multi_part="SINGLE_PART")

        # Rename the output fields to match the original admin field names
        for j, admin_field in enumerate(admin_fields[:i+1]):
            arcpy.management.AlterField(dissolve_output, f"FIRST_{admin_field}", admin_field)

        # Check if the dissolve was successful and the output exists
        if arcpy.Exists(dissolve_output):
            print(f"Dissolved output created: {dissolve_output}")
            
                    # Optional: Convert the dissolved polygon to a line feature class
        desc = arcpy.Describe(dissolve_output)
        if desc.shapeType == "Polygon":
            line_output = f"{dissolve_output}_lineFC"
            arcpy.management.PolygonToLine(dissolve_output, line_output)

            if arcpy.Exists(line_output):
                print(f"Polygon to line output created: {line_output}")
            else:
                print(f"Failed to create polygon to line output: {line_output}")
        else:
            print(f"The output feature class is not a polygon: {dissolve_output}")

    else:
        print(f"Failed to create dissolved output: {dissolve_output}")

print("done.")
