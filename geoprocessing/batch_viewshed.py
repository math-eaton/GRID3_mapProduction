import arcpy
import os
import math

# Setting the environment
arcpy.env.parallelProcessingFactor = "100%"
workspace = r"D:\mheaton\cartography\gsapp\colloquium_i\colloquium_i.gdb"
arcpy.env.workspace = workspace

# Define input and output parameters
in_raster = "output_USGS30m_NYS_contourExtent_20231126"
observer_points = "Cellular_Towers_NYS_DEM_clip_20231126"
batch_size = 10  # Process 10 inputs per batch

# Function to process viewshed in batches
def process_batch(batch):
    batch_name = f"batch_{batch}"
    out_raster = os.path.join(workspace, f"CellTowers_NYS_viewshed_{batch_name}_20231126")
    arcpy.ddd.Viewshed2(
        in_raster=in_raster,
        in_observer_features=batch_name,
        out_raster=out_raster,
        out_agl_raster=None,
        analysis_type="FREQUENCY",
        vertical_error="0 Meters",
        out_observer_region_relationship_table=None,
        refractivity_coefficient=0.13,
        surface_offset="0 Meters",
        observer_elevation=None,
        observer_offset="AllStruc",
        inner_radius=None,
        inner_radius_is_3d="GROUND",
        outer_radius="45 Miles",
        outer_radius_is_3d="GROUND",
        horizontal_start_angle=0,
        horizontal_end_angle=360,
        vertical_upper_angle=90,
        vertical_lower_angle=-90,
        analysis_method="ALL_SIGHTLINES",
        analysis_target_device="GPU_THEN_CPU"
    )

# Batch processing for three batches
for batch in range(3):  # Only run three batches for the test
    start = batch * batch_size + 1  # OBJECTID is usually 1-indexed
    end = start + batch_size
    print(f"Processing batch {batch+1} of 3...")

    # Create a feature layer for the current batch
    batch_query = f"OBJECTID >= {start} AND OBJECTID < {end}"
    arcpy.management.MakeFeatureLayer(observer_points, f"batch_{batch}", batch_query)
    
    # Process the current batch
    process_batch(batch)

print("Processing complete.")
