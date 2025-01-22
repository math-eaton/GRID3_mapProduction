import arcpy

# Inputs (update these paths based on your data)
gdb_path = r"\\devgriarc0\DdriveDevgriarc0\data\nga\microplans\P3b_malaria_microplans\Ogun_2024\distribution_hubs\toJoin_20241007\fromJoin_20241007.gdb"
polygon_fc = "ogun_settlementType_perWard_poly_20241008"  # Polygon with the 'urbanRural_int_Mode' field
fc_priority_1 = "DP_HF_MatchedJoin_XY_20241007"
fc_priority_2 = "DP_poi_MatchedJoin_XY_20241007"
fc_priority_3 = "DP_settlements_MatchedJoin_XY_20241007"

# Create full paths for feature classes
fc_priority_1_path = f"{gdb_path}\\{fc_priority_1}"
fc_priority_2_path = f"{gdb_path}\\{fc_priority_2}"
fc_priority_3_path = f"{gdb_path}\\{fc_priority_3}"
polygon_fc_path = f"{gdb_path}\\{polygon_fc}"

# Set buffer distances based on urbanRural_int_Mode values
buffer_distances = {
    1: 500,  # Rural
    2: 250,  # Semi-Urban
    3: 125   # Urban
}

# Set environment
arcpy.env.workspace = gdb_path
arcpy.env.overwriteOutput = True

# Step 1: Spatial join the 'urbanRural_int_Mode' values to the points
arcpy.analysis.SpatialJoin(fc_priority_1_path, polygon_fc_path, "priority_1_joined", join_type="KEEP_COMMON", match_option="INTERSECT")
arcpy.analysis.SpatialJoin(fc_priority_2_path, polygon_fc_path, "priority_2_joined", join_type="KEEP_COMMON", match_option="INTERSECT")
arcpy.analysis.SpatialJoin(fc_priority_3_path, polygon_fc_path, "priority_3_joined", join_type="KEEP_COMMON", match_option="INTERSECT")

# Step 2: Apply buffers to each priority points layer based on 'urbanRural_int_Mode'
for priority_layer, output_buffer in [("priority_1_joined", "priority_1_buffer"), 
                                      ("priority_2_joined", "priority_2_buffer"),
                                      ("priority_3_joined", "priority_3_buffer")]:
    # Create a new field for buffer distances and calculate based on 'urbanRural_int_Mode'
    arcpy.AddField_management(priority_layer, "buffer_dist", "DOUBLE")
    arcpy.CalculateField_management(priority_layer, "buffer_dist", 
                                    "500 if !urbanRural_int_Mode! == 1 else (250 if !urbanRural_int_Mode! == 2 else 125)", 
                                    "PYTHON3")
    
    # Buffer the points based on calculated distance
    arcpy.Buffer_analysis(priority_layer, output_buffer, "buffer_dist")

# Step 3: Remove Priority 2 points intersecting Priority 1 buffers
arcpy.MakeFeatureLayer_management("priority_2_joined", "lyr_priority_2")
arcpy.SelectLayerByLocation_management("lyr_priority_2", "INTERSECT", "priority_1_buffer")
arcpy.DeleteFeatures_management("lyr_priority_2")  # Remove intersecting points

# Step 4: Remove Priority 3 points intersecting either Priority 1 or Priority 2 buffers
arcpy.MakeFeatureLayer_management("priority_3_joined", "lyr_priority_3")
arcpy.SelectLayerByLocation_management("lyr_priority_3", "INTERSECT", "priority_1_buffer")
arcpy.SelectLayerByLocation_management("lyr_priority_3", "INTERSECT", "priority_2_buffer", selection_type="ADD_TO_SELECTION")
arcpy.DeleteFeatures_management("lyr_priority_3")  # Remove intersecting points

# Retain the individual de-duplicated layers
arcpy.CopyFeatures_management("lyr_priority_2", f"{gdb_path}\\priority_2_deduped")
arcpy.CopyFeatures_management("lyr_priority_3", f"{gdb_path}\\priority_3_deduped")

# Commented out the merge step so you can inspect and merge manually
# arcpy.Merge_management(["priority_1_joined", "priority_2_deduped", "priority_3_deduped"], output_fc_path)

# Clean up intermediate buffer layers but retain the final de-duplicated layers
arcpy.Delete_management("priority_1_buffer")
arcpy.Delete_management("priority_2_buffer")
arcpy.Delete_management("priority_3_buffer")
arcpy.Delete_management("priority_1_joined")

print("Point thinning complete. Intermediate de-duplicated layers are retained for inspection.")
