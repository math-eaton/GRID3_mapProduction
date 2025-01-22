import arcpy
import os

# Path to your ArcGIS Pro project file
project_path = r"path_to_your_project.aprx"

# Name of the map series
map_series_name = "Your_Map_Series_Name"

# Output folder
output_folder = r"path_to_output_folder"

# Create an ArcGISProject object
aprx = arcpy.mp.ArcGISProject(project_path)

# Get the layout with the map series
layout = aprx.listLayouts()[0]

# Check if map series is enabled
if not layout.mapSeries is None and layout.mapSeries.enabled:
    map_series = layout.mapSeries
    
    # Create a list of unique STATE values
    state_values = set(row.getValue("STATE") for row in arcpy.SearchCursor("Your_Map_Series_Layer"))

    # Loop through the unique STATE values and export pages for each state
    for state in state_values:
        # Set the current page using the page name (STATE)
        map_series.currentPageNumber = map_series.getPageNumberFromName(state)

        # Export the current page to PDF
        output_pdf = os.path.join(output_folder, f"{state}_Pages.pdf")
        map_series.exportToPDF(output_pdf, "CURRENT", resolution=300)

# Clean up
del aprx
