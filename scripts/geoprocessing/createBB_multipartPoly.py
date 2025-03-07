import arcpy
import os

# Set the environment to allow overwriting output
arcpy.env.overwriteOutput = True

# Define your input and output feature classes
input_fc = r"input" 
dissolve_fc = r"scratch"  
output_fc = r"output"  

# Step 1: Dissolve the input polygons by 'pageName' to combine parts of the same multipart polygon.
common_fields = [["pageNumber", "FIRST"], ["pageTotal", "FIRST"]]
arcpy.Dissolve_management(in_features=input_fc,
                          out_feature_class=dissolve_fc,
                          dissolve_field="pageName",
                          common_fields=common_fields)

# Step 2: Generate the minimum bounding rectangle for each dissolved polygon.
arcpy.MinimumBoundingGeometry_management(in_features=dissolve_fc,
                                           out_feature_class=output_fc,
                                           geometry_type="RECTANGLE_BY_AREA",
                                           group_option="NONE",
                                           group_field="",
                                           mbg_fields_option="MBG_FIELDS")

print("Minimum bounding rectangles created at: {}".format(output_fc))
