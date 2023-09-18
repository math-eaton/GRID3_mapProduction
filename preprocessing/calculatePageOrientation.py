import arcpy

# Step 1: Create the minimum bounding rectangle
# Define the input feature class and output feature class
input_feature_class = "YourInputFeatureClass"
output_feature_class = "YourOutputFeatureClass"

# Create the minimum bounding rectangle, preserving attributes
arcpy.MinimumBoundingGeometry_management(input_feature_class, output_feature_class, "RECTANGLE_BY_AREA", "ALL")

# Step 2: Calculate MBG main angle
# Add a new field "MBG_Orientation" to the output feature class
arcpy.AddField_management(output_feature_class, "MBG_Orientation", "DOUBLE")

# Calculate the MBG main angle and store it in the "MBG_Orientation" field
arcpy.CalculateField_management(output_feature_class, "MBG_Orientation", "!MBG_Orientation!", "PYTHON_9.3")

# Step 3: Add a new text field "pageOrientation"
arcpy.AddField_management(output_feature_class, "pageOrientation", "TEXT")

# Step 4: Select records with MBG_orientation value of <45 OR >=135
# Create a SQL expression for the selection
sql_expression = "MBG_Orientation < 45 OR MBG_Orientation >= 135"

# Select the records based on the SQL expression
arcpy.SelectLayerByAttribute_management(output_feature_class, "NEW_SELECTION", sql_expression)

# Step 5: Calculate selected records in pageOrientation as "PORTRAIT"
arcpy.CalculateField_management(output_feature_class, "pageOrientation", "'PORTRAIT'", "PYTHON")

# Step 6: Invert the selection and calculate pageOrientation as "LANDSCAPE"
# Invert the current selection
arcpy.SelectLayerByAttribute_management(output_feature_class, "SWITCH_SELECTION")

# Calculate the inverted selection in pageOrientation as "LANDSCAPE"
arcpy.CalculateField_management(output_feature_class, "pageOrientation", "'LANDSCAPE'", "PYTHON")

# Clear the selection
arcpy.SelectLayerByAttribute_management(output_feature_class, "CLEAR_SELECTION")

# Step 7: Join the "pageOrientation" field back to the original input feature class
# Define the join fields and the join type
join_input = input_feature_class
join_input_field = "YourJoinField"  # Replace with the field used for joining
join_output = output_feature_class
join_output_field = "YourJoinField"  # Replace with the field used for joining
join_type = "KEEP_COMMON"

# Join the fields
arcpy.JoinField_management(join_input, join_input_field, join_output, join_output_field, "pageOrientation")

# Step 8: Add a new "pageOrientation" field to the input feature class
arcpy.AddField_management(input_feature_class, "pageOrientation", "TEXT")

# Step 9: Calculate "pageOrientation (join)" = pageOrientation
arcpy.CalculateField_management(input_feature_class, "pageOrientation", "!pageOrientation_1!", "PYTHON")

# Step 10: Remove the join
arcpy.RemoveJoin_management(join_input, join_output)

# Cleanup: Delete the intermediate output feature class if needed
# arcpy.Delete_management(output_feature_class)
