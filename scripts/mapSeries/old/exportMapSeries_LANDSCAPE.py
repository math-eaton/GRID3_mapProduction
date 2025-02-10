import arcpy
import os
import sys

# Define the path to your ArcGIS Pro project (.aprx)
project_path = r"your_project_path_here.aprx"

# Define variables for page size, orientation, use case, and page name
page_size = "A0"  # Example: Change this to your desired page size
orientation = "LANDSCAPE"
use_case = "Your_Use_Case"  # Example: Specify your use case
page_name = "<pageName>"  # This will be replaced with the actual page name

# Load the ArcGIS Pro project
p = arcpy.mp.ArcGISProject(project_path)

# Define the name of the field in the index layer to customize
index_layer_field = "pageOrientation"

# Find layouts that contain the word "landscape" in their names
matching_layouts = []


# Iterate through all layouts in the project
for layout in p.listLayouts():
    if not layout.mapSeries is None and layout.mapSeries.enabled:
        index_layer = layout.mapSeries.indexLayer
        
        # Select features with the specified pageOrientation value
        arcpy.management.SelectLayerByAttribute(index_layer, "NEW_SELECTION", f"{index_layer_field} = 'LANDSCAPE'")
        
        # Check if any features are selected
        if int(arcpy.GetCount_management(index_layer).getOutput(0)) > 0:
            # Add the layout to the list of matching layouts
            matching_layouts.append(layout)

# Export selected features for each "LANDSCAPE" layout
for layout in matching_layouts:
    ms = layout.mapSeries
    
    # Get the page name from the map series
    page_name = ms.pageName
    
    # Define the output PDF file name
    output_pdf = os.path.join(os.path.dirname(sys.argv[0]), relpath, f"{page_size}_{orientation}_{use_case}_{page_name}.pdf")
    
    # Export selected features as PDF at 300 DPI
    ms.exportToPDF(output_pdf, "SELECTED", resolution=300)

# Clean up
del p
