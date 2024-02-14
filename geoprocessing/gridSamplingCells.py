import arcpy
import math
import os
import random  # Use 'random' instead of 'math.random'

# Set the workspace - Update this path to your project's geodatabase
arcpy.env.workspace = r"D:\mheaton\cartography\gsapp\colloquium_i\nys_grid_subsetting\input_raw.gdb"
arcpy.env.overwriteOutput = True

# Inputs
input_polygon = "study_area_true_usaClip"  # Name of the input polygon feature class
output_grid = "sample_cells"  # Name for the output grid feature class
output_gdb = r"D:\mheaton\cartography\gsapp\colloquium_i\nys_grid_subsetting\output_clipped.gdb"  # Path to the output geodatabase

# Grid Index Features parameters
polygonWidth = "25 kilometers"  # Adjust as needed
polygonHeight = "25 kilometers"  # Adjust as needed
samplePercentage = 5

# Step 1: Create Grid Index Features using the ArcPy Cartography tool
arcpy.cartography.GridIndexFeatures(out_feature_class=output_grid, 
                                    in_features=input_polygon, 
                                    polygon_width=polygonWidth, 
                                    polygon_height=polygonHeight)

# Step 2: Extract a random sample of the grid cells
grid_cells = [row[0] for row in arcpy.da.SearchCursor(output_grid, "OID@")]
sample_size = int(len(grid_cells) * (samplePercentage / 100.0))  
sampled_cells = random.sample(grid_cells, sample_size)  

# Create a new feature class for sampled cells
sampled_grid = os.path.join(output_gdb, "sampled_grid")
arcpy.management.CreateFeatureclass(output_gdb, "sampled_grid", "POLYGON", template=output_grid)

# Insert the sampled cells into the new feature class
with arcpy.da.InsertCursor(sampled_grid, ["SHAPE@"]) as insert_cursor:
    where_clause = f"OID IN ({','.join(map(str, sampled_cells))})"
    with arcpy.da.SearchCursor(output_grid, ["SHAPE@"], where_clause=where_clause) as search_cursor:
        for row in search_cursor:
            insert_cursor.insertRow(row)

# Step 3: Clip and export features for each sampled grid cell
feature_classes = arcpy.ListFeatureClasses()  # List all feature classes in the input geodatabase
for cell_id in sampled_cells:
    where_clause = f"OID = {cell_id}"
    with arcpy.da.SearchCursor(output_grid, ["SHAPE@"], where_clause=where_clause) as cursor:
        for row in cursor:
            cell_shape = row[0]
            for fc in feature_classes:
                output_fc_name = f"{fc}_clip_{cell_id}"
                output_fc_path = os.path.join(output_gdb, output_fc_name)
                arcpy.analysis.Clip(fc, cell_shape, output_fc_path)

print("done.")
