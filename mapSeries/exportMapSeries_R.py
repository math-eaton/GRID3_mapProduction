import arcpy
import os
import sys
import re
from datetime import datetime

# Define variables for use case and resolution
use_case = "reference"
resolution = 300
layout_size = "A2"

# Function to format the current date in YYYYMMDD format
def get_current_date_format():
    return datetime.now().strftime('%Y%m%d')

# Define the path to your pro project and
# name of custom output directory
project_path = r"E:\\mheaton\\cartography\\COD_EAF_reference_microplanning_consolidation_20241121\\COD_EAF_reference_microplanning_consolidation_20241205.aprx"
output_foldername = f"OUTPUT_{layout_size}_{use_case}_{get_current_date_format()}"
output_directory = os.path.join(os.path.dirname(project_path), output_foldername)

# Check if the output directory exists, and if not, create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Define keywords for filtering
layout_keywords = ["a2_reference"]
map_series_keywords = ["RDC_Sankuru"]
orientation_keywords = None  # Example: ["LANDSCAPE", "PORTRAIT"]

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

def export_layout(layout, output_path, format):
    """Exports the given layout to the specified format with comparable settings."""
    if format.lower() == "jpg":
        layout.exportToJPEG(output_path, resolution=resolution, jpeg_quality=75)
    elif format.lower() == "pdf":
        layout.exportToPDF(output_path, resolution=resolution, image_quality='BETTER', 
                           compress_vector_graphics=True, image_compression='JPEG', embed_fonts=True,
                           layers_attributes='NONE', georef_info=False, jpeg_compression_quality=75, 
                           output_as_image=False, embed_color_profile=True)

export_format = "jpg"  # "pdf" or "jpg"
exported_pages = {}

for layout in p.listLayouts():
    if layout.mapSeries and layout.mapSeries.enabled and layout_matches_keywords(layout):
        ms = layout.mapSeries
        index_layer = ms.indexLayer
        orientation_field_exists = field_exists(index_layer, "ORIENTATION")
        name_field = ms.pageNameField.name if hasattr(ms.pageNameField, 'name') else ms.pageNameField

        # Retrieve start and end page numbers from command-line arguments
        start_page = int(sys.argv[1]) if len(sys.argv) > 1 else 1
        end_page = int(sys.argv[2]) if len(sys.argv) > 2 else ms.pageCount

        print(f"Processing layout: {layout.name}")
        print(f"Start page: {start_page}, End page: {end_page}, Total pages: {ms.pageCount}")

        for pageNum in range(start_page, end_page + 1):
            ms.currentPageNumber = pageNum
            print(f"Processing Map Series Page: {pageNum}")

            original_page_name = getattr(ms.pageRow, str(name_field))
            page_name = sanitize_filename(original_page_name).upper()

            # Skip already exported pages
            if page_name in exported_pages:
                print(f"Skipping already exported page: {page_name}")
                continue

            # Check if orientation field exists and obtain its value if it does
            page_orientation = getattr(ms.pageRow, "overlaps_txt", None)
            page_orientation = page_orientation.upper() if page_orientation else None

            page_start_time = datetime.now()


            # Apply page filtering based on keywords and optional orientation keywords
            if page_matches_keywords(page_name) and (
                not orientation_keywords or not orientation_field_exists or
                any(keyword.lower() == page_orientation.lower() for keyword in orientation_keywords)):

                # Get the ObjectID field name for the index layer
                object_id_field = arcpy.Describe(index_layer).OIDFieldName

                # Get the ObjectID of the current pageRow
                object_id = getattr(ms.pageRow, object_id_field)

                # Query the feature using the ObjectID to get its geometry
                with arcpy.da.SearchCursor(index_layer, ["SHAPE@"], f"{object_id_field} = {object_id}") as cursor:
                    for row in cursor:
                        geometry = row[0]
                        part_count = geometry.partCount

                        if part_count > 1:  # Multipart polygon
                            for part_index in range(part_count):
                                unique_page_number = part_index + 1
                                if (page_name, unique_page_number) in exported_pages:
                                    continue

                                exported_pages[(page_name, unique_page_number)] = True

                                # Generate filename for this part
                                base_output_name = f"{layout_size}_{use_case}_{page_name}_{unique_page_number}_{get_current_date_format()}"
                                output_name = f"{base_output_name}.{export_format}"
                                output_path = os.path.join(output_directory, output_name)

                                export_layout(layout, output_path, export_format)
                                print(f"Exported: {output_name} (Part {unique_page_number})")

                        else:  # Single-part polygon
                            unique_page_number = 1
                            if (page_name, unique_page_number) in exported_pages:
                                continue

                            exported_pages[(page_name, unique_page_number)] = True

                            # Generate filename for the single-part polygon
                            base_output_name = f"{layout_size}_{use_case}_{page_name}_{unique_page_number}_{get_current_date_format()}"
                            output_name = f"{base_output_name}.{export_format}"
                            output_path = os.path.join(output_directory, output_name)

                            export_layout(layout, output_path, export_format)
                            print(f"Exported: {output_name}")

                page_end_time = datetime.now()
                page_creation_time = page_end_time - page_start_time
                total_elapsed_time = page_end_time - script_start_time

                print(f"Exported: {output_name} to {output_directory}")
                print(f"Page creation time: {page_creation_time}")
                print(f"Total elapsed time: {total_elapsed_time}")
                print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

del p
print("done.")