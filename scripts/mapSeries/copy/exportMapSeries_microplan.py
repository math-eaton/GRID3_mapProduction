import arcpy
import os
import sys
import re
from datetime import datetime

# Define variables for use case and resolution
use_case = "reference"
resolution = 300
layout_size = "A2"

# Optional logic to skip map generation if file already exists
skip_if_exists = False

# Function to format the current date in YYYYMMDD format
def get_current_date_format():
    return datetime.now().strftime('%Y%m%d')

# Define the path to your pro project and name of custom output directory
project_path = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\COD_EAF_reference_microplanning_consolidation_20241205.aprx"
output_foldername = f"OUTPUT_{layout_size}_{use_case}_{get_current_date_format()}"
output_directory = os.path.join(os.path.dirname(project_path), output_foldername)
# output_directory = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\OUTPUT_A2_microplanification_20241213_rename"


# Check if the output directory exists, and if not, create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Define keywords for filtering
layout_keywords = ["a2_microplanification"]
# map_series_keywords = ["Mongala"]
map_series_keywords = ["ALL"]
orientation_keywords = None

# Load the ArcGIS Pro project
p = arcpy.mp.ArcGISProject(project_path)
script_start_time = datetime.now()

# Function to check if the layout matches specified keywords
def layout_matches_keywords(layout):
    if not layout_keywords:
        return True
    return any(keyword.lower() in layout.name.lower() for keyword in layout_keywords)

# Function to check if the map series page matches specified keywords
def page_matches_keywords(page_name):
    if not map_series_keywords or map_series_keywords == ["ALL"]:
        return True
    return any(keyword.lower() in page_name.lower() for keyword in map_series_keywords)

# Function to check for the existence of a field in a layer
def field_exists(layer, field_name):
    return field_name in [f.name for f in arcpy.ListFields(layer)]

def sanitize_filename(name):
    name = name.encode('ascii', 'ignore').decode()
    forbidden_chars = r'[\\/*?:"<>| ]'
    name = re.sub(forbidden_chars, '', name)
    return name

def unique_filename(directory, name, extension):
    filename = f"{name}{extension}"
    filepath = os.path.join(directory, filename)
    counter = 1
    while os.path.exists(filepath):
        filename = f"{name}_{counter}{extension}"
        filepath = os.path.join(directory, filename)
        counter += 1
    return filename

def export_layout(layout, output_path, format):
    """Exports the given layout to the specified format."""
    if format.lower() == "jpg":
        layout.exportToJPEG(output_path, resolution=resolution, jpeg_quality=75)
    elif format.lower() == "pdf":
        layout.exportToPDF(output_path, resolution=resolution, image_quality='BETTER', 
                           compress_vector_graphics=True, image_compression='JPEG', embed_fonts=True,
                           layers_attributes='NONE', georef_info=False, jpeg_compression_quality=75, 
                           output_as_image=False, embed_color_profile=True)

export_format = "jpg"  # "pdf" or "jpg"
exported_count = 0

for layout in p.listLayouts():
    if layout.mapSeries and layout.mapSeries.enabled and layout_matches_keywords(layout):
        ms = layout.mapSeries
        index_layer = ms.indexLayer
        name_field = ms.pageNameField.name if hasattr(ms.pageNameField, 'name') else ms.pageNameField

        # Check if "pageTotal" field exists
        pageTotal_field_exists = field_exists(index_layer, "pageTotal")

        start_page = int(sys.argv[1]) if len(sys.argv) > 1 else 1
        end_page = int(sys.argv[2]) if len(sys.argv) > 2 else ms.pageCount

        for pageNum in range(start_page, end_page + 1):
            ms.currentPageNumber = pageNum
            print(f"Processing Map Series Page: {pageNum}")
            original_page_name = getattr(ms.pageRow, str(name_field))

            page_name = sanitize_filename(original_page_name).upper()

            # If the pageTotal field exists, retrieve its value
            if pageTotal_field_exists:
                pageTotal_value = getattr(ms.pageRow, "pageTotal", None)
            else:
                pageTotal_value = None

            # Apply the filtering condition: pageTotal must be > 1 if the field exists
            if pageTotal_value is not None and pageTotal_value <= 1:
                print(f"Page {page_name} (PageNum {pageNum}) skipped because pageTotal <= 1.")
                continue

            # Additional keyword filters
            if page_matches_keywords(page_name):
                base_output_name = f"{layout_size}_{page_name}_{use_case}_{get_current_date_format()}"
                main_filename = f"{base_output_name}.{export_format}"
                main_output_path = os.path.join(output_directory, main_filename)

                if skip_if_exists and os.path.exists(main_output_path):
                    print(f"File {main_filename} already exists. Skipping map generation for {page_name}.")
                    continue
                else:
                    if not skip_if_exists:
                        output_name = unique_filename(output_directory, base_output_name, f".{export_format}")
                        output_path = os.path.join(output_directory, output_name)
                    else:
                        # If skip_if_exists is True and file doesn't exist yet
                        output_path = main_output_path

                    page_start_time = datetime.now()
                    export_layout(layout, output_path, export_format)
                    page_end_time = datetime.now()
                    page_creation_time = page_end_time - page_start_time
                    total_elapsed_time = page_end_time - script_start_time

                    print(f"Exported: {os.path.basename(output_path)} to {output_directory}")
                    print(f"Page creation time: {page_creation_time}")
                    print(f"Total elapsed time: {total_elapsed_time}")
                    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

del p
print("done.")
