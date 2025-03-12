import arcpy
import os
from datetime import datetime
arcpy.env.overwriteOutput = True

def get_current_date():
    return datetime.now().strftime("%Y%m%d")
current_date = get_current_date()

input_fc = r"E:\mheaton\cartography\GRID_2025\RDC_EAF_2025\data\20250214\processed\processed.gdb\GRID3_COD_health_areas_v4_0_pagename_airesante_dissolved"
dissolve_fc = r"E:\mheaton\cartography\GRID_2025\RDC_EAF_2025\data\20250214\scratch\scratch.gdb\aireSante_MPBB_scratch_{}".format(current_date)
output_fc = r"E:\mheaton\cartography\GRID_2025\RDC_EAF_2025\data\20250214\processed\processed.gdb\GRID3_COD_health_areas_v4_0_MPBB_{}".format(current_date)  # Final output feature class

dissolve_field = "pagename_airesante"

# Create a feature layer from the input, selecting only records where pageTotal > 1
input_layer = "input_layer"
where_clause = '"pageTotal" > 1'
arcpy.MakeFeatureLayer_management(input_fc, input_layer, where_clause)

# Dynamically build a list of all input fields (except system fields) with the FIRST statistic
exclude_fields = ['OBJECTID', 'Shape', 'SHAPE']
fields = arcpy.ListFields(input_fc)
common_fields = []

for field in fields:
    if field.name.upper() not in [ex.upper() for ex in exclude_fields]:
        common_fields.append([field.name, "FIRST"])

# Dissolve the input layer by pageName, transferring all fields using the dynamic common_fields list
arcpy.Dissolve_management(in_features=input_layer,
                          out_feature_class=dissolve_fc,
                          dissolve_field=dissolve_field,
                          statistics_fields=common_fields)

# Loop through the fields of the dissolved feature class and strip the "FIRST_" prefix from names and aliases
for field in arcpy.ListFields(dissolve_fc):
    if field.name.startswith("FIRST_"):
        new_name = field.name[len("FIRST_"):]
        new_alias = field.aliasName
        if new_alias.startswith("FIRST_"):
            new_alias = new_alias[len("FIRST_"):]
        try:
            arcpy.AlterField_management(dissolve_fc, field.name,
                                        new_field_name=new_name,
                                        new_field_alias=new_alias)
        except Exception as e:
            arcpy.AddWarning("Could not alter field {}: {}".format(field.name, e))

# Generate the minimum bounding rectangle for each dissolved polygon
arcpy.MinimumBoundingGeometry_management(in_features=dissolve_fc,
                                           out_feature_class=output_fc,
                                           geometry_type="RECTANGLE_BY_AREA",
                                           group_option="NONE",
                                           group_field="",
                                           mbg_fields_option="MBG_FIELDS")

print("Minimum bounding rectangles created at: {}".format(output_fc))
