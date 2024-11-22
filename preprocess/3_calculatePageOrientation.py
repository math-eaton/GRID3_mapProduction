import arcpy
from arcpy import env

env.overwriteOutput = True

# Helper function to dynamically get the full field name after a join
def get_joined_field_name(joined_feature_class, field_name):
    joined_base_name = arcpy.Describe(joined_feature_class).baseName
    full_field_name = "{}.{}".format(joined_base_name, field_name)
    return full_field_name

# Define input and output feature classes
input_feature_class = r"E:\mheaton\cartography\COD_PEV_smallScale_overviews_20241007\data\merged.gdb\merged_polygon_zonesante_dissolved"
output_feature_class = r"E:\mheaton\cartography\COD_PEV_smallScale_overviews_20241007\data\merged.gdb\merged_polygon_zonesante_dissolved_ORIENTATION"

# Create the minimum bounding rectangle
# TODO: ditto common field name
arcpy.MinimumBoundingGeometry_management(input_feature_class, output_feature_class, "RECTANGLE_BY_AREA", "LIST", "pagename_zonesante", "MBG_FIELDS")
# arcpy.MinimumBoundingGeometry_management(input_feature_class, output_feature_class, "RECTANGLE_BY_AREA", "LIST", "pagename_province", "MBG_FIELDS")
# arcpy.MinimumBoundingGeometry_management(input_feature_class, output_feature_class, "RECTANGLE_BY_AREA", "LIST", "pagename_antenne", "MBG_FIELDS")


# Identify the main angle field
fields = arcpy.ListFields(output_feature_class)
main_angle_field = None
for field in fields:
    if 'Angle' in field.name or 'Orient' in field.name:
        main_angle_field = field.name
        break

if not main_angle_field:
    raise ValueError("Main angle field not found in the output feature class.")

# Add and calculate MBG_Orientation field
arcpy.AddField_management(output_feature_class, "MBG_Orientation", "DOUBLE")
arcpy.CalculateField_management(output_feature_class, "MBG_Orientation", f"!{main_angle_field}!", "PYTHON_9.3")

# Add a new text field for page orientation
arcpy.AddField_management(output_feature_class, "pageOrientation", "TEXT")

# Create a layer from the output feature class
arcpy.MakeFeatureLayer_management(output_feature_class, "output_layer")

# Select records with MBG_Orientation < 45 OR >= 135 for "PORTRAIT"
sql_expression = "MBG_Orientation < 45 OR MBG_Orientation >= 135"
arcpy.SelectLayerByAttribute_management("output_layer", "NEW_SELECTION", sql_expression)
print("Count of PORTRAIT records:", arcpy.GetCount_management("output_layer"))
arcpy.CalculateField_management("output_layer", "pageOrientation", "'PORTRAIT'", "PYTHON_9.3")

# Switch selection to select "LANDSCAPE"
arcpy.SelectLayerByAttribute_management("output_layer", "SWITCH_SELECTION")
print("Count of LANDSCAPE records:", arcpy.GetCount_management("output_layer"))
arcpy.CalculateField_management("output_layer", "pageOrientation", "'LANDSCAPE'", "PYTHON_9.3")

# Clear the selection
arcpy.SelectLayerByAttribute_management("output_layer", "CLEAR_SELECTION")

# Create layers from input and output feature classes
arcpy.MakeFeatureLayer_management(input_feature_class, "input_layer")
arcpy.MakeFeatureLayer_management(output_feature_class, "output_layer")

# Perform the join operation - TODO: make common field name more flexible
arcpy.AddJoin_management("input_layer", "pagename_zonesante", "output_layer", "pagename_zonesante", "KEEP_COMMON")
# arcpy.AddJoin_management("input_layer", "pagename_province", "output_layer", "pagename_province", "KEEP_COMMON")
# arcpy.AddJoin_management("input_layer", "pagename_antenne", "output_layer", "pagename_antenne", "KEEP_COMMON")


# Use the helper function to get the full field name for 'pageOrientation' in the output layer
full_field_name_output = get_joined_field_name(output_feature_class, "pageOrientation")
print("Full field name after join:", full_field_name_output)

# Add a new field for the calculated orientation
arcpy.AddField_management("input_layer", "pageOrientation_New", "TEXT")

# Perform the field calculation
arcpy.CalculateField_management("input_layer", "pageOrientation_New", f"!{full_field_name_output}!", "PYTHON_9.3")

# Remove the join from the input layer
arcpy.RemoveJoin_management("input_layer", arcpy.Describe(output_feature_class).baseName)

# Clean up: delete temporary layers and fields
arcpy.Delete_management("input_layer")
arcpy.Delete_management("output_layer")

# Delete the original pageOrientation field
arcpy.DeleteField_management(input_feature_class, "pageOrientation")

# Rename "pageOrientation_New" to "pageOrientation" and set the alias
arcpy.AlterField_management(input_feature_class, "pageOrientation_New", "pageOrientation", "pageOrientation")

print("done.")
