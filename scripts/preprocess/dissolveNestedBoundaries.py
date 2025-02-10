import arcpy
import os

arcpy.env.overwriteOutput = True

# Set up the workspace and input feature class
workspace = r'D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\raw\COD_raw_MN_MG_TS_2024.gdb'
arcpy.env.workspace = workspace
input_layer = 'GRID3_COD_TP_MG_aireSante_2040109'

# Define the output feature classes
output_gdb = r'D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\processing\boundaries.gdb'
output_admin_0 = 'TP_MG_province'
output_admin_1 = 'TP_MG_zone_sante'
output_admin_2 = 'TP_MG_aire_sante'

# Define statistics fields
statistics_fields = [('aire_sante', 'FIRST'), ('zone_sante', 'FIRST'), ('province', 'FIRST')]

# Function to update field names and aliases
def update_field_names_and_aliases(output_layer, old_new_names):
    for old_name, new_name in old_new_names:
        arcpy.AlterField_management(output_layer, old_name, new_name, new_name)

# Dissolve and update fields for each output layer
for dissolve_field, output_layer in [('province', output_admin_0), ('zone_sante', output_admin_1), ('aire_sante', output_admin_2)]:
    output_path = os.path.join(output_gdb, output_layer)
    arcpy.Dissolve_management(input_layer, output_path, dissolve_field, statistics_fields=statistics_fields)

    # Delete dissolve field
    arcpy.DeleteField_management(output_path, dissolve_field)

    # Update field names and aliases
    updated_field_names = [('FIRST_aire_sante', 'aire_sante'), ('FIRST_zone_sante', 'zone_sante'), ('FIRST_province', 'province')]
    update_field_names_and_aliases(output_path, updated_field_names)

    print(f"Dissolve process for '{dissolve_field}' completed.")

print("All processes completed.")
