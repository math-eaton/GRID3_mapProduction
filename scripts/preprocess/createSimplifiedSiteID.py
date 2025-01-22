import arcpy
from arcpy import env
env.overwriteOutput = True

# Define input feature class
input_fc = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_KS-MG-TP_20241219\data\20241220\processed\processed.gdb\SN_HK_TP_KO_KS_all_sites_merge_20241222_pagename"

# Add necessary fields if they don't exist
fields_to_add = [
    ("Calc", "TEXT"),
    ("siteID", "TEXT"),
    ("sitename", "TEXT")
]

for field_name, field_type in fields_to_add:
    if field_name not in [f.name for f in arcpy.ListFields(input_fc)]:
        arcpy.AddField_management(input_fc, field_name, field_type)
        print(f"Added field: {field_name}")

# Sort the input feature class
print("Sorting feature class...")
sorted_fc = arcpy.management.Sort(
    input_fc, 
    r"E:\mheaton\cartography\COD_EAF_reference_microplanning_KS-MG-TP_20241219\data\20241220\processed\processed.gdb\sites_ID_sorted_fc_20241222", 
    [["pagename_airesante", "ASCENDING"], ["global_rank", "ASCENDING"]]
)
print("Sorting complete.")

# Generate the Calc field and sequential numbering (pre-truncation)
print("Generating 'Calc' field (before truncation)...")
cursor_fields = ["pagename_airesante", "global_rank", "Calc"]
current_page = None
sequential_id = 0

with arcpy.da.UpdateCursor(sorted_fc, cursor_fields) as cursor:
    for row in cursor:
        pagename = row[0]
        global_rank = row[1]

        if pagename is None:
            print("Skipping row with null pagename_airesante.")
            continue

        # Reset sequential ID for a new pagename_airesante
        if pagename != current_page:
            current_page = pagename
            sequential_id = 0
        else:
            sequential_id += 1

        # Handle cases where global_rank is None
        suffix = sequential_id

        # Create Calc field content (full pagename with suffix)
        calc_value = f"{pagename}_{suffix}"
        row[2] = calc_value
        cursor.updateRow(row)
        print(f"Updated Calc (pre-truncation): {calc_value}")

# Generate siteID from Calc field (post-truncation)
print("Generating 'siteID' from 'Calc' field...")
cursor_fields = ["Calc", "siteID"]

with arcpy.da.UpdateCursor(sorted_fc, cursor_fields) as cursor:
    for row in cursor:
        calc = row[0]
        if calc:
            parts = calc.split("_")  # Split Calc field by '_'

            if len(parts) >= 5:  # Ensure there are enough parts
                zonesante_part = parts[3][:2]  # First 2 characters of the fourth part
                airesante_part = parts[4][:2]  # First 2 characters of the fifth part
                sequential_part = parts[-1]  # The last part (sequential number)

                # Generate siteID
                site_id = f"{zonesante_part}{airesante_part}_{sequential_part}"
                row[1] = site_id
                cursor.updateRow(row)
                print(f"Generated siteID (post-truncation): {site_id}")
            else:
                print(f"Skipping Calc value (too few parts): {calc}")

# Update sitename based on session_type
print("Updating 'sitename' field...")
cursor_fields = ["session_type", "ESSnom1", "siteID", "sitename"]

with arcpy.da.UpdateCursor(sorted_fc, cursor_fields) as cursor:
    for row in cursor:
        session_type = row[0]
        essnom1 = row[1]
        site_id = row[2]

        if session_type == "fixed":  # If session_type is FIXED
            row[3] = essnom1  # Copy ESSnom1 to sitename
            print(f"Set sitename to ESSnom1: {essnom1}")
        else:  # Otherwise, copy siteID to sitename
            row[3] = site_id
            print(f"Set sitename to siteID: {site_id}")

        cursor.updateRow(row)

print("Processing complete.")
