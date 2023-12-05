import arcpy
import math
import os
import datetime

def log_time(start_time, step_description):
    """ Log the current and elapsed time for a given step """
    current_time = datetime.datetime.now()
    elapsed_time = current_time - start_time
    print(f"{step_description} completed at {current_time.strftime('%Y-%m-%d %H:%M:%S')}. Elapsed time: {elapsed_time}")

# Record the start time
start_time = datetime.datetime.now()

# Set the environment settings
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

# Define inputs
input_raster = "path_to_input_raster"  # Replace with the path to your input raster
output_points = "path_to_output_points"  # Replace with the path to store output points
output_polygons = "path_to_output_polygons"  # Replace with the path to store output polygons
elevation_raster = "path_to_elevation_raster"  # Replace with the path to your elevation raster
cell_size = 500  # Define the cell size for resampling

# Task 1: Resample the input raster
resampled_raster = arcpy.management.Resample(in_raster=input_raster, 
                                             out_raster="in_memory/resampled", 
                                             cell_size=cell_size, 
                                             resampling_type="NEAREST")
log_time(start_time, "Resampling raster")

# Task 2: Convert the raster to points
arcpy.conversion.RasterToPoint(in_raster=resampled_raster, 
                               out_point_features=output_points, 
                               raster_field="Value")

# Calculate the hypotenuse of the raster cell
aggregation_distance = math.sqrt(2 * cell_size ** 2)

log_time(start_time, "Raster to points conversion")

# Task 3: Aggregate points into polygons
arcpy.cartography.AggregatePoints(Point_Features=output_points, 
                                  Out_Polygon_Features=output_polygons, 
                                  Aggregation_Distance=aggregation_distance, 
                                  Processing_Cell_Size=cell_size)
log_time(start_time, "Aggregate points")

# Task 4: Add a field "Group_ID" to the RasterToPoints layer
arcpy.management.AddField(in_table=output_points, 
                          field_name="Group_ID", 
                          field_type="LONG")
log_time(start_time, "Adding Group_ID field")

# Task 5: Spatially join the points to the polygons to get the Group_ID
arcpy.analysis.SpatialJoin(target_features=output_points, 
                           join_features=output_polygons, 
                           out_feature_class="in_memory/joined_points", 
                           join_operation="JOIN_ONE_TO_ONE", 
                           join_type="KEEP_ALL", 
                           match_option="INTERSECT")
log_time(start_time, "Spatial join for Group_ID")

# Task 6: Add Surface Information (elevation) to the points
arcpy.ddd.AddSurfaceInformation(in_feature_class="in_memory/joined_points", 
                                in_surface=elevation_raster, 
                                out_property="Z")
log_time(start_time, "Adding surface information")

# Task 7: Save the points as a formatted GeoJSON file in WGS84
output_geojson = os.path.splitext(output_points)[0] + ".geojson"
arcpy.management.Project(in_dataset="in_memory/joined_points", 
                         out_dataset=output_geojson, 
                         out_coor_system="WGS 1984")
log_time(start_time, "Exporting to GeoJSON")

# Export to GeoJSON
arcpy.conversion.FeaturesToJSON(in_features=output_geojson, 
                                out_json_file=output_geojson, 
                                format_json="FORMATTED", 
                                include_z="true")

# Check in the Spatial Analyst extension
arcpy.CheckInExtension("Spatial")

log_time(start_time, "All geoprocessing tasks completed successfully.")