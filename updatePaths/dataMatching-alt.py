import arcpy
import csv

# Set your workspace to the folder containing the new geodatabase
arcpy.env.workspace = r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010"

# Define the path to your new geodatabase
# new_geodatabase = r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\processed\COD_Maniema-Mongala-Tschopo_microplanning_20231010.gdb"

# Access your ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject("D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\COD_Maniema-Mongala-Tschopo_microplanning_20231010.aprx")

# Load the CSV file with updated data sources
csv_file = r"D:\GRID\DRC\Cartography\COD_Maniema-Mongala-Tschopo_microplanning_20231010\data\dictionary.csv"

# Create dictionaries to map LayerName to new data sources and new layer names
data_source_mapping = {}
layer_name_mapping = {}

# Read the CSV file and populate the mapping dictionaries
with open(csv_file, "r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        data_source_mapping[row["LayerName"]] = row["DataSource"]
        layer_name_mapping[row["LayerName"]] = row["NewLayerName"]

# Iterate through the map(s) in your project
for map in aprx.listMaps():
    # Create a list to store the layer names and data source paths
    layer_info = []

    # Iterate through layers in the map
    for layer in map.listLayers():
        # Check if the layer is a feature layer
        if layer.isFeatureLayer:
            new_data_source = data_source_mapping.get(layer.name)
            new_layer_name = layer_name_mapping.get(layer.name)

            if new_data_source:
                # Update the layer's data source
                layer.updateConnectionProperties(layer.connectionProperties, new_data_source)
                
                # Update layer name if a new name exists in the CSV
                if new_layer_name:
                    layer.name = new_layer_name

                layer_info.append((layer.name, layer.dataSource, new_data_source))

    # Print the layer information for this map
    print(f"Layers updated in map '{map.name}':")
    for name, _, new_source in layer_info:
        print(f"  Layer Name: {name}")
        print(f"  New Data Source: {new_source}")
        print()

# Save the changes to your project
aprx.save()
