import arcpy
import csv
import os

arcpy.env.overwriteOutput = True

# Set your workspace to the folder containing the project
arcpy.env.workspace = r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010"

# Access your ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject(r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\COD_Maniema-Mongala-Tschopo_microplanning_updates_202401.aprx")

# Create a list to store layer information
layer_info = []

# Iterate through the map(s) in your project
for map in aprx.listMaps():
    # Iterate through layers in the map
    for layer in map.listLayers():
        # Check if the layer is a feature layer
        if layer.isFeatureLayer:
            try:
                # Attempt to access layer properties
                data_source = layer.dataSource
            except Exception:
                # If an error occurs, the layer is likely broken
                data_source = "Broken Link"

            layer_info.append({
                "MapName": map.name,
                "LayerName": layer.name,
                "DataSource": data_source
            })

# Define the output CSV file path
output_file = os.path.join(arcpy.env.workspace, "data", "dictionary.csv")

# Save the layer information to the output CSV file
with open(output_file, "w", newline="") as file:
    csv_writer = csv.DictWriter(file, fieldnames=["MapName", "LayerName", "DataSource"])
    csv_writer.writeheader()
    csv_writer.writerows(layer_info)

print("done.")
