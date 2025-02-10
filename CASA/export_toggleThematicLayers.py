import arcpy
import os
import re
from datetime import datetime

# Define variables for use case and resolution
resolution = 300
layout_size = "A2"
# Optional keywords to filter layouts (leave as None to process all layouts)
layout_keywords = ["CITY_VULNERABILITY"]  # Add your keywords here

# Function to format the current date in YYYYMMDD format
def get_current_date_format():
    return datetime.now().strftime('%Y%m%d')

# Define the path to your pro project and
# name of custom output directory
project_path = r"E:\mheaton\cartography\CASA_cartography\CASA_cartography.aprx"
output_foldername = f"OUTPUT_{layout_size}_{layout_keywords}_{get_current_date_format()}"
output_directory = os.path.join(os.path.dirname(project_path), output_foldername)

# Check if the output directory exists, and if not, create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    print(f"Created output directory: {output_directory}")
else:
    print(f"Using existing output directory: {output_directory}")

# Function to sanitize filenames (removes forbidden characters)
def sanitize_filename(name):
    name = name.encode('ascii', 'ignore').decode()
    forbidden_chars = r'[\\/*?:"<>| ]'
    name = re.sub(forbidden_chars, '_', name)  # Replaces forbidden characters with underscore
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
    print(f"Exported layout to {output_path} as {format.upper()}")

# Function to check if the layout matches specified keywords
def layout_matches_keywords(layout):
    if not layout_keywords:
        return True
    return any(keyword.lower() in layout.name.lower() for keyword in layout_keywords)

# Function to export only the legend as a separate PDF for each thematic layer and page
def export_legend_solo(layout, legend, page_name, thematic_layer, output_directory, export_format="pdf"):
    # Hide all elements except the legend
    for element in layout.listElements():
        if element.name != legend.name:
            element.visible = False

    # Export the legend as a standalone PDF
    sanitized_legend_name = sanitize_filename(f"{layout.name}_{page_name}_{thematic_layer}_Legend")
    output_legend_filename = unique_filename(output_directory, sanitized_legend_name, f".{export_format}")
    export_layout(layout, output_legend_filename, export_format)

    # Restore visibility of all elements after export
    for element in layout.listElements():
        element.visible = True

    print(f"Exported standalone legend for {page_name} with {thematic_layer} to {output_legend_filename}")

# Main script starts here
print(f"Opening project: {project_path}")
aprx = arcpy.mp.ArcGISProject(project_path)  # Path to your project

# Loop through each layout in the project and export its map series
for lyt in aprx.listLayouts():
    # Check if the layout matches the provided keywords (or process all if None)
    if layout_matches_keywords(lyt):
        print(f"\nProcessing layout: {lyt.name}")

        # Get the map series for the current layout
        ms = lyt.mapSeries

        if ms is None or ms.pageCount == 0:
            print(f"No map series found for layout: {lyt.name}")
            continue

        print(f"Found map series with {ms.pageCount} pages in layout: {lyt.name}")

        # List of common layers to keep visible (e.g., basemap, admin boundaries)
        common_layers = [
            "ADMIN0", 
            "ADMIN0_DeepDive_PairwiseDissolve",
            "World Hillshade",
            "World Terrain Base"
        ]
        print(f"Common layers: {common_layers}")

        # Get the map object for this layout
        m = lyt.listElements("MAPFRAME_ELEMENT", "*")[0].map  # Gets the first map frame's map
        print(f"Accessed map frame for layout: {lyt.name}")

        # Dynamically create the list of thematic layers by excluding common layers
        thematic_layers = [layer.name for layer in m.listLayers() if layer.name not in common_layers]
        print(f"Thematic layers: {thematic_layers}")

        # Access the legend element in the layout (assumes "Legend" is its name)
        legend_element = lyt.listElements("LEGEND_ELEMENT", "Legend")[0]

        # Export maps for each combination of map series page (study area) and thematic layer
        export_format = "pdf"  # Set export format, e.g., 'pdf'
        for i in range(ms.pageCount):
            ms.currentPageNumber = i + 1  # Set to current map series page

            # Get the name of the current map series page (study area)
            current_page_name = ms.pageRow.GADM_NAME_0_cleaned  # replace with map series index FIELD name
            sanitized_page_name = sanitize_filename(current_page_name)
            print(f"\nProcessing page {ms.currentPageNumber}: {current_page_name}")

            # Loop through each thematic layer for this page
            for thematic_layer in thematic_layers:
                # Set all thematic layers to invisible first
                for layer in thematic_layers:
                    lyr = m.listLayers(layer)[0]
                    lyr.visible = False

                # Make the current thematic layer visible
                lyr = m.listLayers(thematic_layer)[0]
                lyr.visible = True
                sanitized_layer_name = sanitize_filename(thematic_layer)

                # Generate a unique filename with the page and thematic layer name
                output_filename = unique_filename(
                    output_directory, 
                    f"{lyt.name}_{sanitized_page_name}_{sanitized_layer_name}", 
                    f".{export_format}"
                )
                print(f"Generating map for {current_page_name} with theme {thematic_layer}")

                # Export the layout
                export_layout(lyt, output_filename, export_format)

                # Now export the legend synchronized with the thematic layer
                export_legend_solo(lyt, legend_element, sanitized_page_name, sanitized_layer_name, output_directory, export_format)

        print(f"Completed export for layout: {lyt.name}")

print("All maps and legends exported.")
