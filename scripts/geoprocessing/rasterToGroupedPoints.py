import arcpy
import math
import os
import datetime

def log_time(start_time, step_description):
    """ Log the current and elapsed time for a given step """
    current_time = datetime.datetime.now()
    elapsed_time = current_time - start_time
    print(f"{step_description} completed at {current_time.strftime('%Y-%m-%d %H:%M:%S')}. Elapsed time: {elapsed_time}")

def run_geoprocessing_tasks():
    try:
        # Record the start time
        start_time = datetime.datetime.now()

        # Set the environment settings
        arcpy.env.overwriteOutput = True
        arcpy.CheckOutExtension("Spatial")

        # Define inputs
        input_raster = r"D:\mheaton\cartography\gsapp\colloquium_i\rasterToPoints_20231205.gdb\Merged_Viewshed_NYS_Resample_Reclassify_20231204"  # Replace with the path to your input raster
        elevation_raster = r"D:\mheaton\cartography\gsapp\colloquium_i\data\NYS_DEM\output_USGS30m.tif"
        cell_size = 2500  # Define the cell size for resampling

        # Define the base path for output features
        base_output_path = r"D:\mheaton\cartography\gsapp\colloquium_i\rasterToPoints_20231205.gdb"

        # Get the spatial reference from the input raster
        input_spatial_ref = arcpy.Describe(input_raster).spatialReference

        # Define the scratch workspace (e.g., a file geodatabase for temporary data)
        scratch_workspace = r"D:\mheaton\cartography\gsapp\colloquium_i\scratch.gdb"  # Replace with your scratch workspace path
        arcpy.env.scratchWorkspace = scratch_workspace

        # Task 1: Resample the input raster
        resampled_raster = os.path.join(scratch_workspace, "resampled")
        arcpy.management.Resample(in_raster=input_raster, 
                                  out_raster=resampled_raster, 
                                  cell_size=cell_size, 
                                  resampling_type="NEAREST")
        log_time(start_time, "Resampling raster")

        # Task 2: Convert the raster to points
        output_points = os.path.join(scratch_workspace, f"output_points_{cell_size}")
        arcpy.conversion.RasterToPoint(in_raster=resampled_raster, 
                                    out_point_features=output_points, 
                                    raster_field="Value")

        # Task 2.1: Create a Z-enabled feature class
        z_enabled_points = "in_memory/z_enabled_points"
        arcpy.management.CreateFeatureclass(out_path=os.path.dirname(z_enabled_points),
                                            out_name=os.path.basename(z_enabled_points),
                                            geometry_type="POINT",
                                            has_z="ENABLED",
                                            spatial_reference=input_spatial_ref)  # Use the input's spatial reference


        # Task 2.2: Copy the points to the Z-enabled feature class
        arcpy.management.CopyFeatures(output_points, z_enabled_points)

        log_time(start_time, "Raster to points conversion")

        # Task 3: Aggregate points into polygons
        aggregated_polygons = os.path.join(scratch_workspace, f"aggregated_polygons_{cell_size}")
        relationship_table = aggregated_polygons + "_Tbl"
        aggregation_distance = math.sqrt(2 * cell_size ** 2)
        arcpy.cartography.AggregatePoints(in_features=output_points, 
                                        out_feature_class=aggregated_polygons, 
                                        aggregation_distance=aggregation_distance)
        log_time(start_time, "Aggregate points")

        # Task 4: Add a field "Group_ID" to the RasterToPoints layer
        arcpy.management.AddField(in_table=output_points, 
                                field_name="Group_ID", 
                                field_type="LONG")
        log_time(start_time, "Adding Group_ID field")

        # Task 5: Join the relationship table to the points and calculate Group_ID
        arcpy.management.JoinField(in_data=output_points, 
                                in_field="OBJECTID", 
                                join_table=relationship_table, 
                                join_field="INPUT_FID", 
                                fields="OUTPUT_FID")
        arcpy.management.CalculateField(in_table=output_points, 
                                        field="Group_ID", 
                                        expression="!OUTPUT_FID!", 
                                        expression_type="PYTHON3")
        log_time(start_time, "Joining and calculating Group_ID")

         # Task 6: Add Surface Information (elevation) to the points
        arcpy.ddd.AddSurfaceInformation(in_feature_class=output_points, 
                                        in_surface=elevation_raster, 
                                        out_property="Z")
        log_time(start_time, "Adding surface information")

        # Task 7: Export the points as a formatted GeoJSON file in WGS 84
        geojson_output_path = r"D:\mheaton\cartography\gsapp\colloquium_i\scriptOutput_2500.geojson"
        arcpy.conversion.FeaturesToJSON(in_features=output_points, 
                                        out_json_file=geojson_output_path, 
                                        format_json="FORMATTED", 
                                        include_z_values="Z_VALUES",
                                        outputToWGS84="WGS84",
                                        geoJSON="GEOJSON")

        log_time(start_time, "Exporting to GeoJSON")
                                        
        # Check in the Spatial Analyst extension
        arcpy.CheckInExtension("Spatial")

        log_time(start_time, "All geoprocessing tasks completed successfully.")



    except Exception as e:
        arcpy.AddError(str(e))
        print(f"Error occurred: {e}")

# Run the geoprocessing tasks
run_geoprocessing_tasks()