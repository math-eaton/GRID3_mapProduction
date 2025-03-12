import arcpy
import os
import sys
import re
from datetime import datetime

# Define variables for use case and resolution
use_case = "reference"
resolution = 300
layout_size = "A2"

export_date = datetime.now().strftime('%Y%m%d')

# Path to your ArcGIS Pro project
project_path = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_KS-MG-TP_20241219\COD_EAF_reference_microplanning_MONGALA_20250109_refCopy.aprx"
output_foldername = f"OUTPUT_{layout_size}_{use_case}_{export_date}"
output_directory = os.path.join(os.path.dirname(project_path), output_foldername)

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Define keywords for filtering
layout_keywords = ["a2_reference"]
map_series_keywords = ["ALL"]
orientation_keywords = None  # Example: ["LANDSCAPE", "PORTRAIT"]

# Load the ArcGIS Pro project
p = arcpy.mp.ArcGISProject(project_path)
script_start_time = datetime.now()

def layout_matches_keywords(layout):
    """Return True if the layout name matches any of the layout_keywords."""
    if not layout_keywords:
        return True
    return any(keyword.lower() in layout.name.lower() for keyword in layout_keywords)

def page_matches_keywords(page_name):
    """Return True if the page_name matches any of the map_series_keywords."""
    if not map_series_keywords or map_series_keywords == ["ALL"]:
        return True
    return any(keyword.lower() in page_name.lower() for keyword in map_series_keywords)

def field_exists(layer, field_name):
    """Check if a given field_name exists in the layer."""
    return field_name in [f.name for f in arcpy.ListFields(layer)]

def sanitize_filename(name):
    """Remove or replace any characters that could cause filesystem issues."""
    name = name.encode('ascii', 'ignore').decode()
    forbidden_chars = r'[\\/*?:"<>| ]'
    name = re.sub(forbidden_chars, '', name)
    return name

def export_layout(layout, output_path, fmt):
    """Exports the given layout to JPEG/PDF, with consistent settings."""
    if fmt.lower() == "jpg":
        layout.exportToJPEG(
            output_path,
            resolution=resolution,
            jpeg_quality=75
        )
    elif fmt.lower() == "pdf":
        layout.exportToPDF(
            output_path,
            resolution=resolution,
            image_quality='BETTER',
            compress_vector_graphics=True,
            image_compression='JPEG',
            embed_fonts=True,
            layers_attributes='NONE',
            georef_info=False,
            jpeg_compression_quality=75,
            output_as_image=False,
            embed_color_profile=True
        )

export_format = "jpg"  # or "pdf"
exported_pages = set()  # track exported pages so we don’t repeat work

# Retrieve start and end page numbers from command-line arguments
start_page = int(sys.argv[1]) if len(sys.argv) > 1 else 1
end_page = None
if len(sys.argv) > 2:
    end_page = int(sys.argv[2])

for layout in p.listLayouts():
    if layout.mapSeries and layout.mapSeries.enabled and layout_matches_keywords(layout):
        ms = layout.mapSeries
        index_layer = ms.indexLayer

        # Check required fields
        pageNum_field = "pageNum"
        if not field_exists(index_layer, pageNum_field):
            print(f"ERROR: The index layer does not contain the required field '{pageNum_field}'.")
            print(f"Skipping layout: {layout.name}\n")
            continue

        orientation_field_exists = field_exists(index_layer, "ORIENTATION")
        name_field = ms.pageNameField.name if hasattr(ms.pageNameField, 'name') else ms.pageNameField

        # If end_page was not specified, default it to the total pageCount
        final_page = end_page if end_page else ms.pageCount

        print(f"Processing layout: {layout.name}")
        print(f"Start page: {start_page}, End page: {final_page}, Total pages: {ms.pageCount}")

        for page_index in range(start_page, final_page + 1):
            ms.currentPageNumber = page_index
            print(f"Processing Map Series Page: {page_index}")

            original_page_name = getattr(ms.pageRow, str(name_field))
            part_id = getattr(ms.pageRow, pageNum_field)  # e.g., an integer or part index

            # Build a unique page_name with the preprocessed part ID
            page_name = sanitize_filename(original_page_name).upper() + "_" + str(part_id)

            # Skip if we've already exported this name
            if page_name in exported_pages:
                print(f"Skipping already exported page: {page_name}")
                continue

            # (Optional) orientation logic
            page_orientation = getattr(ms.pageRow, "overlaps_txt", None)
            page_orientation = page_orientation.upper() if page_orientation else None

            page_start_time = datetime.now()

            # Evaluate filtering by name/keywords/orientation
            if page_matches_keywords(page_name) and (
                not orientation_keywords or not orientation_field_exists or
                any(keyword.lower() == page_orientation.lower() for keyword in orientation_keywords)):

                # Mark as exported so we don't duplicate
                exported_pages.add(page_name)

                # Build output filenames
                base_output_name = f"{layout_size}_{use_case}_{page_name}_{export_date}"
                output_name = f"{base_output_name}.{export_format}"
                output_path = os.path.join(output_directory, output_name)

                # Export the layout
                export_layout(layout, output_path, export_format)
                print(f"Exported: {output_name}")

                # Timing analytics
                page_end_time = datetime.now()
                page_creation_time = page_end_time - page_start_time
                total_elapsed_time = page_end_time - script_start_time

                print(f"Exported: {output_name} to {output_directory}")
                print(f"Page creation time: {page_creation_time}")
                print(f"Total elapsed time: {total_elapsed_time}")
                print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

del p
print("done.")
