import arcpy
from arcpy import env

env.overwriteOutput = True

#TODO fix join back to index layer

# Helper function to dynamically get the full field name after a join
def get_joined_field_name(joined_feature_class, field_name):
    # Get the base name of the joined feature class
    joined_base_name = arcpy.Describe(joined_feature_class).baseName

    # Construct the joined field name
    full_field_name = "{}.{}".format(joined_base_name, field_name)
    return full_field_name

# 1: Create the minimum bounding rectangle
# Define the input feature class and output feature class
input_feature_class = r"D:\GRID\NGA\map_production\NGA_Gombe-Ogun_202402\data\processing\scratch.gdb\jigawa_mapIndex_20240229"
output_feature_class = r"D:\GRID\NGA\map_production\NGA_Gombe-Ogun_202402\data\processing\scratch.gdb\jigawa_mapIndex_orientation_20240229"

# Create the minimum bounding rectangle, preserving attributes and generating separate MBG for each feature
arcpy.MinimumBoundingGeometry_management(input_feature_class, output_feature_class, "RECTANGLE_BY_AREA", "LIST", "pagename", "MBG_FIELDS")

# 2: Calculate MBG main angle
# Add a new field "MBG_Orientation" to the output feature class
arcpy.AddField_management(output_feature_class, "MBG_Orientation", "DOUBLE")

# Calculate the MBG main angle and store it in the "MBG_Orientation" field
arcpy.CalculateField_management(output_feature_class, "MBG_Orientation", "!MBG_Orientation!", "PYTHON_9.3")

# 3: Add a new text field "pageOrientation"
arcpy.AddField_management(output_feature_class, "pageOrientation", "TEXT")

# 4: Select records with MBG_orientation value of <45 OR >=135

# Create a layer from the output feature class
arcpy.MakeFeatureLayer_management(output_feature_class, "output_layer")

# Use the created layer for selection
sql_expression = "MBG_Orientation < 45 OR MBG_Orientation >= 135"
arcpy.SelectLayerByAttribute_management("output_layer", "NEW_SELECTION", sql_expression)

# Select the records based on the SQL expression
# Select records for "PORTRAIT"
print("Count of PORTRAIT records:", arcpy.GetCount_management("output_layer"))

# Calculate "PORTRAIT"
arcpy.CalculateField_management("output_layer", "pageOrientation", "'PORTRAIT'", "PYTHON")

# Select records for "LANDSCAPE"
arcpy.SelectLayerByAttribute_management("output_layer", "SWITCH_SELECTION")
print("Count of LANDSCAPE records:", arcpy.GetCount_management("output_layer"))

# Calculate "LANDSCAPE"
arcpy.CalculateField_management("output_layer", "pageOrientation", "'LANDSCAPE'", "PYTHON")

# Clear the selection
arcpy.SelectLayerByAttribute_management("output_layer", "CLEAR_SELECTION")

# Join the 'pageOrientation' field back to the original input feature class
join_input = input_feature_class
join_output_field = "pagename"  # Adjust the field name as per your data
join_type = "KEEP_COMMON"

# Create a layer from the input feature class (if not already created)
arcpy.MakeFeatureLayer_management(input_feature_class, "input_layer")

###############

# Ensure the join is successful and fields are properly referenced
arcpy.MakeFeatureLayer_management(output_feature_class, "output_layer")
arcpy.MakeFeatureLayer_management(input_feature_class, "input_layer")

# Perform the join operation
arcpy.AddJoin_management("input_layer", join_output_field, "output_layer", join_output_field, join_type)

# Use the helper function to get the correct full field name for 'pageOrientation' in the output layer
full_field_name_output = get_joined_field_name(output_feature_class, "pageOrientation")

# Verify the field name is correct
print("Full field name after join: ", full_field_name_output)

# Add the new field for calculation
arcpy.AddField_management("input_layer", "pageOrientation_New", "TEXT")

# Perform the field calculation
arcpy.CalculateField_management("input_layer", "pageOrientation_New", "!" + full_field_name_output + "!", "PYTHON")

############

# Remove the join from the input layer
arcpy.RemoveJoin_management("input_layer", arcpy.Describe(output_feature_class).baseName)

# Delete the temporary layers if no longer needed
arcpy.Delete_management("input_layer")
arcpy.Delete_management("output_layer")

# 13: Delete the original pageOrientation field (from the join)
arcpy.DeleteField_management(input_feature_class, "pageOrientation")

# 14: Rename "pageOrientation_New" to "pageOrientation"
arcpy.AlterField_management(input_feature_class, "pageOrientation_New", "pageOrientation")

print("done.")