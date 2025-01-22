import arcpy

# Set environment settings
arcpy.env.overwriteOutput = True

# Input feature class and the other parameters
input_fc = r"E:\mheaton\cartography\COD_microplanning_042024\COD_microplanning_042024.gdb\MN_as_opt_20240515_ExportTable_XYTableToPoint"
output_gdb = r"E:\mheaton\cartography\COD_microplanning_042024\data\thiessen.gdb"
ess_polygon_fc = r"E:\mheaton\cartography\COD_microplanning_042024\data\consolidated\consolidated.gdb\Ogun_hf_walk_based_catchments_20240430"

# List to store intermediate and final outputs
intermediate_outputs = []

print("Starting script...")

# Get unique priority values
print("Retrieving unique priority values...")
priorities = set(row[0] for row in arcpy.da.SearchCursor(input_fc, ["priority"]))

for priority in priorities:
    print(f"Processing priority: {priority}")

    # Create a layer from the input feature class
    arcpy.management.MakeFeatureLayer(input_fc, "input_layer")

    # Select points with the current priority
    print(f"  Selecting points for priority: {priority}")
    arcpy.management.SelectLayerByAttribute("input_layer", "NEW_SELECTION", f"priority = {priority}")
    
    # Create Thiessen polygons
    thiessen_polygons = f"in_memory/thiessen_{priority}"
    print(f"  Creating Thiessen polygons for priority: {priority}")
    arcpy.analysis.CreateThiessenPolygons("input_layer", thiessen_polygons, "ALL")
    arcpy.management.AddField(thiessen_polygons, "priority", "LONG")
    arcpy.management.CalculateField(thiessen_polygons, "priority", f"{priority}", "PYTHON3")

    # Create 3 km buffer
    buffer_polygons = f"in_memory/buffer_{priority}"
    print(f"  Creating 3 km buffer for priority: {priority}")
    arcpy.analysis.Buffer("input_layer", buffer_polygons, "3 Kilometers")
    arcpy.management.AddField(buffer_polygons, "priority", "LONG")
    arcpy.management.CalculateField(buffer_polygons, "priority", f"{priority}", "PYTHON3")

    # Clip Thiessen polygons to buffer
    clipped_polygons = f"in_memory/clipped_{priority}"
    print(f"  Clipping Thiessen polygons to buffer for priority: {priority}")
    arcpy.analysis.Clip(thiessen_polygons, buffer_polygons, clipped_polygons)
    intermediate_outputs.append(clipped_polygons)

    # Clean up the temporary layer
    arcpy.management.Delete("input_layer")

# Merge all clipped outputs
merged_output = f"{output_gdb}/merged_clipped_polygons"
print("Merging all clipped outputs...")
arcpy.management.Merge(intermediate_outputs, merged_output)

# Save the merged output
final_output = f"{output_gdb}/final_output"
print(f"Saving merged output to {final_output}...")
arcpy.management.CopyFeatures(merged_output, final_output)

print("Script completed successfully. Final output is located at:", final_output)
