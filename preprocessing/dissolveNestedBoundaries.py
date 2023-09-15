import arcpy

# Set up the workspace and input feature class
workspace = r'C:\path\to\your\geodatabase'  # Replace with the path to your geodatabase
arcpy.env.workspace = workspace
input_layer = 'boundaries\\ADMIN_3'  # Replace with the name of your input layer within the geodatabase

# Define the output feature classes
output_gdb = 'boundaries.gdb'  # Geodatabase where the output layers will be saved
output_admin_0 = 'ADMIN_0'
output_admin_1 = 'ADMIN_1'
output_admin_2 = 'ADMIN_2'

# Dissolve based on ADMIN_0 field
arcpy.analysis.Dissolve(input_layer, os.path.join(output_gdb, output_admin_0), 'ADMIN_0')

# Dissolve based on ADMIN_1 field
arcpy.analysis.Dissolve(input_layer, os.path.join(output_gdb, output_admin_1), 'ADMIN_1')

# Dissolve based on ADMIN_2 field
arcpy.analysis.Dissolve(input_layer, os.path.join(output_gdb, output_admin_2), 'ADMIN_2')

print("Dissolve process completed.")
