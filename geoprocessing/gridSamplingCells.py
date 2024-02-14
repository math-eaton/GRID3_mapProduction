import arcpy
import random
import os

# Set the workspace and overwrite output
arcpy.env.workspace = r"D:\mheaton\cartography\gsapp\colloquium_i\nys_grid_subsetting\input_raw.gdb"
arcpy.env.overwriteOutput = True

# Inputs
input_polygon = "study_area_true_usaClip"
output_grid = "sample_cells"
output_gdb = r"D:\mheaton\cartography\gsapp\colloquium_i\nys_grid_subsetting\output_clipped.gdb"
polygonWidth = "25 kilometers"
polygonHeight = "25 kilometers"
samplePercentage = 10

# Create Grid Index Features
arcpy.cartography.GridIndexFeatures(out_feature_class=output_grid, 
                                    in_features=input_polygon, 
                                    polygon_width=polygonWidth, 
                                    polygon_height=polygonHeight)

# Extract a random sample of the grid cells
grid_cells = [row[0] for row in arcpy.da.SearchCursor(output_grid, "OID@")]
sample_size = int(len(grid_cells) * (samplePercentage / 100.0))
sampled_cells = random.sample(grid_cells, sample_size)

# Clip and export features for each sampled grid cell, but merge into a single output feature class per input feature class
feature_classes = arcpy.ListFeatureClasses()

for fc in feature_classes:
    desc = arcpy.Describe(fc)
    input_geometry_type = desc.shapeType  # Get the geometry type of the input feature class
    
    output_fc_name = f"{fc}_clip"
    output_fc_path = os.path.join(output_gdb, output_fc_name)

    # Create the output feature class ensuring the geometry type matches the input feature class
    arcpy.management.CreateFeatureclass(output_gdb, output_fc_name, input_geometry_type, spatial_reference=desc.spatialReference)
    arcpy.management.AddField(output_fc_path, "index_grid", "LONG")

    insert_cursor_fields = ["SHAPE@", "index_grid"] if input_geometry_type.upper() != "POINT" else ["SHAPE@XY", "index_grid"]
    insert_cursor = arcpy.da.InsertCursor(output_fc_path, insert_cursor_fields)
    
    for cell_id in sampled_cells:
        where_clause = f"OID = {cell_id}"
        with arcpy.da.SearchCursor(output_grid, ["SHAPE@"], where_clause=where_clause) as cursor:
            for row in cursor:
                cell_shape = row[0]
                in_memory_fc = "in_memory/clipped"
                arcpy.analysis.Clip(fc, cell_shape, in_memory_fc)
                
                # Explode multipart features to singlepart
                singlepart_fc = "in_memory/singlepart"
                arcpy.MultipartToSinglepart_management(in_memory_fc, singlepart_fc)
                
                # Insert exploded features into the output feature class
                with arcpy.da.SearchCursor(singlepart_fc, ["SHAPE@"]) as singlepart_features:
                    for feature in singlepart_features:
                        if input_geometry_type.upper() == "POINT":
                            insert_cursor.insertRow([feature[0].centroid, cell_id])
                        else:
                            insert_cursor.insertRow([feature[0], cell_id])
    
    del insert_cursor  # Ensure the cursor is closed

print("done.")
