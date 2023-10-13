import arcpy
import csv

# Set your workspace to the folder containing the project
arcpy.env.workspace = r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010"

# Access your ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject("D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\COD_Maniema-Mongala-Tschopo_microplanning_20231010.aprx")

# Create a list to store layer information
layer_info = []

# Iterate through the map(s) in your project
for map in aprx.listMaps():
    # Iterate through layers in the map
    for layer in map.listLayers():
        # Check if the layer is a feature layer
        if layer.isFeatureLayer:
            layer_info.append({
                "MapName": map.name,
                "LayerName": layer.name,
                "DataSource": layer.dataSource
            })

# Define the output CSV file path
output_file = r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\dictionary.csv"

# Save the layer information to the output CSV file
with open(output_file, "w", newline="") as file:
    csv_writer = csv.DictWriter(file, fieldnames=["MapName", "LayerName", "DataSource"])
    csv_writer.writeheader()
    csv_writer.writerows(layer_info)
