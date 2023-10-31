import arcpy

# Set the workspace for convenience
arcpy.env.workspace = "path/to/your/geodatabase.gdb"  # Update this to the path of your geodatabase

# The path to your input contour line feature class
contour_fc = "ContourLineFeatureClass"  # Update this to the name of your contour feature class

# The field which contains contour values
contour_field = "Contour"

# The factor by which you want to downsample (e.g., selecting every 3rd contour line for 30-foot resolution)
n_factor = 3

# SQL expression to select every Nth contour
sql_expression = f"({contour_field} / 10) % {n_factor} = 0"

# The path to the output feature class
output_fc = "ContourLineFeatureClass_Downsampled"  # Choose an appropriate name for the downsampled feature class

# Execute Select to create a new feature class with downsampled contours
arcpy.Select_analysis(contour_fc, output_fc, sql_expression)

print(f"Downsampled feature class created at: {output_fc}")
