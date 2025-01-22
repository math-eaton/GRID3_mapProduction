import arcpy
import os

# Define inputs
gdb_path = r"E:\mheaton\data_processing\gsapp_gis\data\towers_separated_v0.gdb"  # Path to your input geodatabase
output_raster_path = r"E:\mheaton\data_processing\gsapp_gis\data\rasterized_3km_towerBuff_20241018.tif"  # Output raster path
cell_size = 0.1  # Define your desired cell size (10KM in this case)

# Set the workspace
arcpy.env.workspace = gdb_path
arcpy.env.overwriteOutput = True

# List all feature classes (assuming all are polygons) in the geodatabase
feature_classes = arcpy.ListFeatureClasses()

# Temporary list to store raster outputs
rasters = []

# Loop through each feature class
for fc in feature_classes:
    # Add a constant field
    field_name = "constant"
    if not arcpy.ListFields(fc, field_name):
        arcpy.AddField_management(fc, field_name, "SHORT")
    
    # Calculate field (constant value of 1)
    arcpy.CalculateField_management(fc, field_name, 1, "PYTHON3")
    
    # Convert the polygons to a raster using the "constant" field
    raster_output = os.path.join(arcpy.env.scratchGDB, f"{os.path.basename(fc)}_raster")
    arcpy.PolygonToRaster_conversion(fc, field_name, raster_output, cell_assignment="MAXIMUM_AREA", cellsize=cell_size)
    
    # Store the raster output
    rasters.append(raster_output)

# Check if any rasters were created
if len(rasters) > 0:
    # Mosaic all the rasters together using the Mosaic To New Raster tool
    arcpy.MosaicToNewRaster_management(
        rasters,  # Input rasters
        os.path.dirname(output_raster_path),  # Output location
        os.path.basename(output_raster_path),  # Output raster name
        "",  # Spatial reference, leave empty to inherit from input rasters
        "32_BIT_FLOAT",  # Pixel type (32-bit float for raster summation)
        cell_size,  # Cell size
        1,  # Number of bands
        "SUM",  # Mosaic method: use sum to add overlapping cells
        "FIRST"  # Mosaic colormap mode
    )

    print(f"Process complete! Summed raster saved at: {output_raster_path}")
else:
    print("No rasters were generated from the input feature classes.")
