import arcpy
import os
import re
from datetime import datetime

# Define variables for use case and resolution
use_case = "deepDive"
resolution = 300
layout_size = "A4"

# Function to format the current date in YYYYMMDD format
def get_current_date_format():
    return datetime.now().strftime('%Y%m%d')

# Define the path to your pro project and
# name of custom output directory
project_path = r"E:\mheaton\cartography\COD_microplanning_042024\COD_microplanning_052024.aprx"
output_foldername = f"OUTPUT_{layout_size}_{use_case}_{get_current_date_format()}"
output_directory = os.path.join(os.path.dirname(project_path), output_foldername)

# Check if the output directory exists, and if not, create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Function to sanitize filenames (removes forbidden characters)
def sanitize_filename(name):
    name = name.encode('ascii', 'ignore').decode()
    forbidden_chars = r'[\\/*?:"<>| ]'
    name = re.sub(forbidden_chars, '', name)
    return name

# Function to ensure unique filenames by adding a counter if a file exists
def unique_filename(directory, name, extension):
    filename = f"{name}{extension}"
    filepath = os.path.join(directory, filename)
    counter = 1
    while os.path.exists(filepath):
        filename = f"{name}_{counter}{extension}"
        filepath = os.path.join(directory, filename)
        counter += 1
    return filepath

# Function to export the layout to the specified format
def export_layout(layout, output_path, format):
    """Exports the given layout to the specified format with comparable settings."""
    if format.lower() == "jpg":
        layout.exportToJPEG(output_path, resolution=resolution, jpeg_quality=75)
    elif format.lower() == "pdf":
        layout.exportToPDF(output_path, resolution=resolution, image_quality='BEST', 
                           compress_vector_graphics=True, image_compression='JPEG', embed_fonts=True,
                           layers_attributes='NONE', georef_info=False, jpeg_compression_quality=75, 
                           output_as_image=False, embed_color_profile=True)

# Main script starts here
aprx = arcpy.mp.ArcGISProject(project_path)  # Path to your project
m = aprx.listMaps("YourMapName")[0]  # Replace with your map's name

lyt = aprx.listLayouts("YourLayoutName")[0]  # Replace with your layout's name
ms = lyt.mapSeries

# List of common layers to keep visible (e.g., basemap, admin boundaries)
common_layers = [
    "Basemap",  # Replace with the actual name(s) of common layers
    "Admin Boundaries"
]

# Dynamically create the list of thematic layers by excluding common layers
thematic_layers = [layer.name for layer in m.listLayers() if layer.name not in common_layers]

# Export map series pages
export_format = "pdf"  # Set export format, e.g., 'pdf'
for i in range(ms.pageCount):
    ms.currentPageNumber = i + 1  # Set to current map series page
    
    # Loop through thematic layers, and toggle visibility
    for thematic_layer in thematic_layers:
        lyr = m.listLayers(thematic_layer)[0]
        lyr.visible = False  # Set all thematic layers to invisible

    # Make only one thematic layer visible per page
    visible_layer = thematic_layers[i % len(thematic_layers)]  # Cycling through layers
    lyr = m.listLayers(visible_layer)[0]
    lyr.visible = True

    # Sanitize the visible layer name for safe use in filenames
    sanitized_layer_name = sanitize_filename(visible_layer)

    # Generate a unique filename using the toggled thematic layer as a suffix
    output_filename = unique_filename(output_directory, f"map_page_{ms.currentPageNumber}_{sanitized_layer_name}", f".{export_format}")
    
    # Export the layout
    export_layout(lyt, output_filename, export_format)

    print(f"Exported page {ms.currentPageNumber} with {visible_layer} visible to {output_filename}")

print("Exporting complete.")
