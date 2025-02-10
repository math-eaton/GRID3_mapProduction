import arcpy
import sys

# Define the path to your pro project
project_path = r"E:\mheaton\cartography\COD_microplanning_042024\COD_microplanning_052024.aprx"

# Define keywords for filtering
layout_keywords = ["reference"]
map_series_keywords = ["Maniema"]
orientation_keywords = ["LANDSCAPE"]

def layout_matches_keywords(layout):
    if not layout_keywords:
        return True
    return any(keyword.lower() in layout.name.lower() for keyword in layout_keywords)

def page_matches_keywords(page_name):
    if not map_series_keywords:
        return True
    return any(keyword.lower() in page_name.lower() for keyword in map_series_keywords)

def orientation_matches_keywords(page_orientation):
    if not orientation_keywords:
        return True
    if page_orientation is None:
        return False
    return any(keyword.lower() == page_orientation.lower() for keyword in orientation_keywords)

def field_exists(layer, field_name):
    return field_name in [f.name for f in arcpy.ListFields(layer)]

def count_matching_pages():
    try:
        p = arcpy.mp.ArcGISProject(project_path)
        total_matching_pages = 0

        for layout in p.listLayouts():
            if layout.mapSeries and layout.mapSeries.enabled and layout_matches_keywords(layout):
                ms = layout.mapSeries
                index_layer = ms.indexLayer
                orientation_field_exists = field_exists(index_layer, "ORIENTATION")
                name_field = ms.pageNameField.name if hasattr(ms.pageNameField, 'name') else ms.pageNameField

                for pageNum in range(1, ms.pageCount + 1):
                    ms.currentPageNumber = pageNum
                    original_page_name = getattr(ms.pageRow, str(name_field))
                    page_name = original_page_name.upper()
                    page_orientation = getattr(ms.pageRow, "ORIENTATION", None)
                    page_orientation = page_orientation.upper() if page_orientation else None

                    if page_matches_keywords(page_name) and (not orientation_field_exists or orientation_matches_keywords(page_orientation)):
                        total_matching_pages += 1

        del p
        return total_matching_pages
    except Exception as e:
        print(f"Error counting matching pages: {e}", file=sys.stderr)
        return -1

if __name__ == "__main__":
    total_pages = count_matching_pages()
    print(total_pages)
