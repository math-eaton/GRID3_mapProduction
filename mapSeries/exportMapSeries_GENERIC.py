import arcpy
import os
import sys
import re
from datetime import datetime

# Define the path to your ArcGIS Pro project (.aprx)
project_path = r"D:\GRID\NGA\map_production\NGA_Gombe-Ogun_202402\microplanning_projects\NGA_Jigawa_microplanning_WARDLEVEL_SATELLITE_20240229.aprx"

# Optional: Define keywords for layout selection, e.g., "LANDSCAPE" or "PORTRAIT"
# If specified, the script will also select map series pages matching these keywords in the pageOrientation field. else leave empty []
# layout_keywords = ["LANDSCAPE", "PORTRAIT"]
layout_keywords = []


# Define variables for use case and resolution
use_case = "microplanning"
resolution = 286  # Specify the resolution
layout_size = "A2"

# Define the maximum number of PDFs to export for testing purposes
max_exports = 2

# Load the ArcGIS Pro project
p = arcpy.mp.ArcGISProject(project_path)

# Start timing the script
script_start_time = datetime.now()

# Function to format the current date in YYYYMMDD format
def get_current_date_format():
    return datetime.now().strftime('%Y%m%d')

# Function to check if the layout matches specified keywords
def layout_matches_keywords(layout):
    if not layout_keywords:  # If layout_keywords list is empty, consider all layouts
        return True
    return any(keyword.lower() in layout.name.lower() for keyword in layout_keywords)

# Function to check for the existence of a field in a layer
def field_exists(layer, field_name):
    return field_name in [f.name for f in arcpy.ListFields(layer)]

def sanitize_filename(name):
    """Remove whitespace, forbidden, and non-ASCII characters."""
    # Remove non-ASCII characters
    name = name.encode('ascii', 'ignore').decode()
    # Remove forbidden characters and whitespace
    forbidden_chars = r'[\\/*?:"<>| ]'  # Add or remove characters based on your OS and requirements
    name = re.sub(forbidden_chars, '', name)
    return name

def unique_filename(directory, name, extension):
    """Ensure filename uniqueness in the given directory by appending a sequential character."""
    filename = f"{name}{extension}"
    filepath = os.path.join(directory, filename)
    counter = 1
    # If the file exists, append a counter to the name until it's unique
    while os.path.exists(filepath):
        filename = f"{name}_{counter}{extension}"
        filepath = os.path.join(directory, filename)
        counter += 1
    return filename


exported_count = 0  # Initialize counter for exported PDFs

for layout in p.listLayouts():
    if layout.mapSeries and layout.mapSeries.enabled and layout_matches_keywords(layout):
        ms = layout.mapSeries
        index_layer = ms.indexLayer
        page_orientation_exists = field_exists(index_layer, "pageOrientation")

        # Correct way to obtain the name_field as a string
        name_field = ms.pageNameField.name if hasattr(ms.pageNameField, 'name') else ms.pageNameField
        
        # Iterate through each page in the map series
        for pageNum in range(1, ms.pageCount + 1):
            if exported_count >= max_exports:  # Check if the export limit is reached
                print(f"Export limit of {max_exports} PDFs reached. Exiting.")
                break  # Break out of the loop once the limit is reached

            ms.currentPageNumber = pageNum
            original_page_name = getattr(ms.pageRow, str(name_field))  # Getting the raw page name

            # Sanitize the page name
            page_name = sanitize_filename(original_page_name).upper()  # Convert to UPPER CASE and sanitize
            
            # Check if page_orientation field exists and obtain its value if it does
            page_orientation = getattr(ms.pageRow, "pageOrientation", "").upper() if page_orientation_exists else None
            
            # Apply filtering based on keyword (e.g. "jigawa" state), layout keywords, and optional page orientation
            if "jigawa".upper() in page_name and (not layout_keywords or (page_orientation and page_orientation in layout_keywords)):
                page_start_time = datetime.now()  # Start timing the page creation

                # Construct the base output filename without the extension
                # base_output_name = f"{layout_size}_{page_name}_{use_case}_{resolution}_{get_current_date_format()}"
                base_output_name = f"{layout_size}_{page_name}_{use_case}_300dpi_{get_current_date_format()}"
                print(base_output_name)

                # Ensure the filename is unique within the output directory
                output_pdf_name = unique_filename(os.path.dirname(sys.argv[0]), base_output_name, ".pdf")  # Use .pdf as the extension
                
                output_pdf_path = os.path.join(os.path.dirname(sys.argv[0]), output_pdf_name)
                print(output_pdf_name)
                print(output_pdf_path)
                
                # Export the current page as PDF
                layout.exportToPDF(output_pdf_path, resolution=resolution)

                
                page_end_time = datetime.now()  # End timing the page creation
                page_creation_time = page_end_time - page_start_time
                total_elapsed_time = page_end_time - script_start_time
                
                print(f"Exported: {output_pdf_name}")
                print(f"Page creation time: {page_creation_time}")
                print(f"Total elapsed time: {total_elapsed_time}")
                print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                exported_count += 1  # Increment the counter after each export
                
                if exported_count >= max_exports:
                    print("Reached the maximum number of exports.")
                    break  # Ensure the loop is exited if the limit is reached

# Clean up
del p
print("done.")