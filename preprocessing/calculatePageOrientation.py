import arcpy
from arcpy import env

env.overwriteOutput = True

# 1: Create the minimum bounding rectangle
# Define the input feature class and output feature class
input_feature_class = "D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\processed\scratch.gdb\GRID3_COD_MA_aire_sante_EK_20230918"
output_feature_class = "D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\processed\scratch.gdb\GRID3_COD_MA_aire_sante_EK_20230918_orientation"

# Create the minimum bounding rectangle, preserving attributes and generating separate MBG for each feature
arcpy.MinimumBoundingGeometry_management(input_feature_class, output_feature_class, "RECTANGLE_BY_AREA", "LIST", "pagename")

# 2: Calculate MBG main angle
# Add a new field "MBG_Orientation" to the output feature class
arcpy.AddField_management(output_feature_class, "MBG_Orientation", "DOUBLE")

# Calculate the MBG main angle and store it in the "MBG_Orientation" field
arcpy.CalculateField_management(output_feature_class, "MBG_Orientation", "!MBG_Angle!", "PYTHON_9.3")

# 3: Add a new text field "pageOrientation"
arcpy.AddField_management(output_feature_class, "pageOrientation", "TEXT")

# 4: Select records with MBG_orientation value of <45 OR >=135
# Create a SQL expression for the selection
sql_expression = "MBG_Orientation < 45 OR MBG_Orientation >= 135"

# Select the records based on the SQL expression
arcpy.SelectLayerByAttribute_management(output_feature_class, "NEW_SELECTION", sql_expression)

# 5: Calculate selected records in pageOrientation as "PORTRAIT"
arcpy.CalculateField_management(output_feature_class, "pageOrientation", "'PORTRAIT'", "PYTHON")

# 6: Invert the selection and calculate pageOrientation as "LANDSCAPE"
# Invert the current selection
arcpy.SelectLayerByAttribute_management(output_feature_class, "SWITCH_SELECTION")

# Calculate the inverted selection in pageOrientation as "LANDSCAPE"
arcpy.CalculateField_management(output_feature_class, "pageOrientation", "'LANDSCAPE'", "PYTHON")

# Clear the selection
arcpy.SelectLayerByAttribute_management(output_feature_class, "CLEAR_SELECTION")

# 7: Join the "pageOrientation" field back to the original input feature class
# Define the join fields and the join type
join_input = input_feature_class
join_input_field = "pagename"  
join_output = output_feature_class
join_output_field = "pagename"  
join_type = "KEEP_COMMON"

import arcpy
from arcpy import env

env.overwriteOutput = True

# 1: Create the minimum bounding rectangle
# Define the input feature class and output feature class
input_feature_class = "D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\processed\scratch.gdb\GRID3_COD_MA_aire_sante_EK_20230918"
output_feature_class = "D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\processed\scratch.gdb\GRID3_COD_MA_aire_sante_EK_20230918_MBG"

# Create the minimum bounding rectangle, preserving attributes and generating separate MBG for each feature
arcpy.MinimumBoundingGeometry_management(input_feature_class, output_feature_class, "RECTANGLE_BY_AREA", "LIST", "pagename")

# 2: Calculate MBG main angle
# Add a new field "MBG_Orientation" to the output feature class
arcpy.AddField_management(output_feature_class, "MBG_Orientation", "DOUBLE")

# Calculate the MBG main angle and store it in the "MBG_Orientation" field
arcpy.CalculateField_management(output_feature_class, "MBG_Orientation", "!MBG_Orientation!", "PYTHON_9.3")

# 3: Add a new text field "pageOrientation"
arcpy.AddField_management(output_feature_class, "pageOrientation", "TEXT")

# 4: Select records with MBG_orientation value of <45 OR >=135
# Create a SQL expression for the selection
sql_expression = "MBG_Orientation < 45 OR MBG_Orientation >= 135"

# Select the records based on the SQL expression
arcpy.SelectLayerByAttribute_management(output_feature_class, "NEW_SELECTION", sql_expression)

# 5: Calculate selected records in pageOrientation as "PORTRAIT"
arcpy.CalculateField_management(output_feature_class, "pageOrientation", "'PORTRAIT'", "PYTHON")

# 6: Invert the selection and calculate pageOrientation as "LANDSCAPE"
# Invert the current selection
arcpy.SelectLayerByAttribute_management(output_feature_class, "SWITCH_SELECTION")

# Calculate the inverted selection in pageOrientation as "LANDSCAPE"
arcpy.CalculateField_management(output_feature_class, "pageOrientation", "'LANDSCAPE'", "PYTHON")

# Clear the selection
arcpy.SelectLayerByAttribute_management(output_feature_class, "CLEAR_SELECTION")

# 7: Join the "pageOrientation" field back to the original input feature class
# Define the join fields and the join type
join_input = input_feature_class
join_input_field = "pagename"  
join_output = output_feature_class
join_output_field = "pagename"  
join_type = "KEEP_COMMON"

# 9: Create a layer from the feature class
arcpy.MakeFeatureLayer_management(join_input, "temp_layer")

# 10: Join the fields using the layer
arcpy.AddJoin_management("temp_layer", join_input_field, join_output, join_output_field, "KEEP_COMMON")

fields = [f.name for f in arcpy.ListFields("temp_layer")]
print(fields)

# 8: Add a new "pageOrientation_New" field to the input feature class to store the independent values
arcpy.AddField_management(input_feature_class, "pageOrientation_New", "TEXT")

# 9: Calculate "pageOrientation_New" = pageOrientation (from the join)
arcpy.CalculateField_management(input_feature_class, "pageOrientation_New", "!pageOrientation!", "PYTHON")

# 10: Create a layer from the feature class
if arcpy.Exists("temp_layer"):
    arcpy.Delete_management("temp_layer")
arcpy.MakeFeatureLayer_management(join_input, "temp_layer")

# 11: Remove the join from the layer
arcpy.RemoveJoin_management("temp_layer", arcpy.Describe(join_output).baseName)

# 12: Optionally delete the layer (if you don't need it later)
arcpy.Delete_management("temp_layer")

# 13: Delete the original pageOrientation field (from the join)
arcpy.DeleteField_management(input_feature_class, "pageOrientation")

# 14: Rename "pageOrientation_New" to "pageOrientation"
arcpy.AlterField_management(input_feature_class, "pageOrientation_New", "pageOrientation")
