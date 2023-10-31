import arcpy

# Set the workspace for convenience
arcpy.env.workspace = r"D:\mheaton\cartography\gsapp\colloquium_i\colloquium_i.gdb"  # Update this to the path of your geodatabase

# The path to your input contour line feature class
contour_fc = "NYS_elevContours_DEMextract_20231031"  # Update this to the name of your contour feature class

# The field which contains contour values
contour_field = "Contour"

# The factor by which you want to downsample (e.g., selecting every 3rd contour line for 30-foot resolution)
n_factor = 10

# SQL expression to select every Nth contour
sql_expression = f"MOD(CAST({contour_field} / 10 AS INT), {n_factor}) = 0"

# The path to the output feature class
output_fc = "NYS_elevContours_DEMextract_downsample_10_20231031"  # Choose an appropriate name for the downsampled feature class

# Execute Select to create a new feature class with downsampled contours
arcpy.Select_analysis(contour_fc, output_fc, sql_expression)

print(f"Downsampled feature class created at: {output_fc}")
