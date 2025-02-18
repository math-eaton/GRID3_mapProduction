import arcpy
import os
import sys
import re
import shutil
from datetime import datetime
import time

# Define variables for use case and resolution
use_case = "reference"
resolution = 300
layout_size = "A2"

# Function to format the current date in YYYYMMDD format
def get_current_date_format():
    return datetime.now().strftime('%Y%m%d')

# Define the original path to your pro project
original_project_path = r"E:\mheaton\cartography\COD_microplanning_042024\COD_microplanning_052024.aprx"

# Create a unique temporary project path for this instance
temp_project_path = os.path.join(os.path.dirname(original_project_path), f"temp_{os.getpid()}_{get_current_date_format()}.aprx")
shutil.copyfile(original_project_path, temp_project_path)

# Define the name of the custom output directory
output_foldername = f"OUTPUT_{layout_size}_{use_case}_{get_current_date_format()}"
output_directory = os.path.join(os.path.dirname(original_project_path), output_foldername)

# Check if the output directory exists, and if not, create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Define keywords for filtering
layout_keywords = ["reference"]
map_series_keywords = ["Maniema"]
orientation_keywords = ["LANDSCAPE"]

# Load the ArcGIS Pro project
p = arcpy.mp.ArcGISProject(temp_project_path)
script_start_time = datetime.now()

# Function to check if the layout matches specified keywords
def layout_matches_keywords(layout):
    if not layout_keywords:
        return True
    return any(keyword.lower() in layout.name.lower() for keyword in layout_keywords)

# Function to check if the map series page matches specified keywords
def page_matches_keywords(page_name):
    if not map_series_keywords:
        return True
    return any(keyword.lower() in page_name.lower() for keyword in map_series_keywords)

# Function to check if the page orientation matches specified keywords
def orientation_matches_keywords(page_orientation):
    if not orientation_keywords:
        return True
    if page_orientation is None:
        return False
    return any(keyword.lower() == page_orientation.lower() for keyword in orientation_keywords)

# Function to check for the existence of a field in a layer
def field_exists(layer, field_name):
    return field_name in [f.name for f in arcpy.ListFields(layer)]

# Function to sanitize filename
def sanitize_filename(name):
    name = name.encode('ascii', 'ignore').decode()
    forbidden_chars = r'[\\/*?:"<>| ]'
    name = re.sub(forbidden_chars, '', name)
    return name

# Function to generate unique filename
def unique_filename(directory, name, extension):
    filename = f"{name}{extension}"
    filepath = os.path.join(directory, filename)
    counter = 1
    while os.path.exists(filepath):
        filename = f"{name}_{counter}{extension}"
        filepath = os.path.join(directory, filename)
        counter += 1
    return filepath

# Function to export layout
def export_layout(layout, output_path, format):
    if format.lower() == "jpg":
        layout.exportToJPEG(output_path, resolution=resolution, jpeg_quality=75)
    elif format.lower() == "pdf":
        layout.exportToPDF(output_path, resolution=resolution, image_quality='BETTER', 
                           compress_vector_graphics=True, image_compression='JPEG', embed_fonts=True,
                           layers_attributes='NONE', georef_info=False, jpeg_compression_quality=75, 
                           output_as_image=False, embed_color_profile=True)

export_format = "pdf"  # Change this to "pdf" if you want to export to PDF

exported_count = 0

# Retrieve start and end page numbers from command-line arguments
start_page = int(sys.argv[1]) if len(sys.argv) > 1 else 1
end_page = int(sys.argv[2]) if len(sys.argv) > 2 else None

# Process each layout
for layout in p.listLayouts():
    if layout.mapSeries and layout.mapSeries.enabled and layout_matches_keywords(layout):
        try:
            ms = layout.mapSeries
            index_layer = ms.indexLayer
            orientation_field_exists = field_exists(index_layer, "ORIENTATION")

            # Safely get the name field
            try:
                name_field = ms.pageNameField.name
            except AttributeError:
                name_field = ms.pageNameField

            # Determine the range of pages to process
            page_range = range(start_page, end_page + 1) if end_page else range(1, ms.pageCount + 1)

            for pageNum in page_range:
                try:
                    ms.currentPageNumber = pageNum
                    original_page_name = getattr(ms.pageRow, str(name_field))

                    # Sanitize the page name
                    page_name = sanitize_filename(original_page_name).upper()

                    # Check if orientation field exists and obtain its value if it does
                    page_orientation = getattr(ms.pageRow, "ORIENTATION", None)
                    page_orientation = page_orientation.upper() if page_orientation else None

                    # Apply page filtering based on keywords, layout keywords, and optional orientation keywords
                    if page_matches_keywords(page_name) and (not orientation_field_exists or orientation_matches_keywords(page_orientation)):
                        try:
                            page_start_time = datetime.now()

                            # Ensure the filename is unique within the custom output directory
                            base_output_name = f"{layout_size}_{page_name}_{use_case}_{get_current_date_format()}"
                            output_path = unique_filename(output_directory, base_output_name, f".{export_format}")

                            # Export the layout
                            export_layout(layout, output_path, export_format)

                            page_end_time = datetime.now()
                            page_creation_time = page_end_time - page_start_time
                            total_elapsed_time = page_end_time - script_start_time

                            print(f"Exported: {output_path} to {output_directory}")
                            print(f"Page creation time: {page_creation_time}")
                            print(f"Total elapsed time: {total_elapsed_time}")
                            print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                        except Exception as e:
                            print(f"Failed to export page {pageNum}: {e}")
                            continue

                except Exception as e:
                    print(f"Failed to process page {pageNum}: {e}")
                    continue

        except Exception as e:
            print(f"Failed to initialize Map Series for layout {layout.name}: {e}")
            continue

# Clean up the project reference
del p

# Wait a few seconds before attempting to delete the temporary project file
time.sleep(5)

# Attempt to delete the temporary project file with retries
max_retries = 5
retry_delay = 5  # seconds

for attempt in range(max_retries):
    try:
        os.remove(temp_project_path)
        print("Temporary project file deleted successfully.")
        break
    except PermissionError:
        if attempt < max_retries - 1:
            print(f"Temporary project file is still in use, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"Failed to delete temporary project file after {max_retries} attempts.")
print("done.")
