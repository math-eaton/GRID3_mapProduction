import arcpy
import math

# Set the workspace (update this to your workspace)
arcpy.env.workspace = "path/to/your/workspace"

# Feature class and field names
feature_class = "your_feature_class"  # Replace with your feature class name
elevation_field = "Z_Value"  # Replace with your elevation field name
threshold_percent = 5  # Percentage threshold for elevation change

# Create a spatial index for efficiency
arcpy.AddSpatialIndex_management(feature_class)

# Compute threshold based on average elevations and percentage
def elevation_change_within_threshold(z1, z2, threshold):
    avg_elevation = (z1 + z2) / 2.0
    percent_change = (abs(z1 - z2) / avg_elevation) * 100
    return percent_change <= threshold

# Get list of OIDs to delete
oids_to_delete = []

# Search cursor to iterate through each point
with arcpy.da.SearchCursor(feature_class, ["OID@", "SHAPE@", elevation_field]) as cursor:
    for row in cursor:
        point = row[1]
        elevation = row[2]

        # Create a query to select nearby points
        distance = 2000  # Distance in meters
        query = f"SHAPE IS WITHIN A DISTANCE OF {distance} METERS FROM '{point.JSON}'"

        # Inner cursor to check nearby points
        with arcpy.da.SearchCursor(feature_class, ["OID@", elevation_field], query) as inner_cursor:
            for inner_row in inner_cursor:
                # Skip the same point
                if inner_row[0] == row[0]:
                    continue

                neighbor_elevation = inner_row[1]
                # Check if the elevation change is within the threshold
                if elevation_change_within_threshold(elevation, neighbor_elevation, threshold_percent):
                    oids_to_delete.append(row[0])
                    break

# Delete the points
with arcpy.da.UpdateCursor(feature_class, ["OID@"]) as del_cursor:
    for del_row in del_cursor:
        if del_row[0] in oids_to_delete:
            del_cursor.deleteRow()

print(f"Deleted {len(oids_to_delete)} points based on the elevation threshold.")