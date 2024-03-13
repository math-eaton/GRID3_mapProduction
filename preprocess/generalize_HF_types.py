import arcpy

# Set environment settings
arcpy.env.workspace = r"D:\GRID\NGA\map_production\NGA_Gombe-Ogun_202402\data\raw\NGA_202402_consolidated.gdb"
arcpy.env.overwriteOutput = True


# Define the path to your feature class
feature_class = "gombe_consolidated_hf_no_private_20240313"

# Define the mapping of generalization categories to specific keywords
# Each key in the dictionary represents the generalized category,
# and the value is a list of specific keywords that fall under that category.
generalizations_nigeria = {
    "hospital": ["hospital"],
    "health center": ["center", "primary", "care"],
    "health post": ["post"],
    "dispensary": ["dispensary", "pharmacy"],
    "clinic": ["clinic", "polyclinic"]
}

# generalizations_drc = {
#     "hospital": ["hospital"],
#     "health center": ["center", "primary", "care"],
#     "health post": ["post"],
#     "dispensary": ["dispensary", "pharmacy"],
#     "clinic": ["clinic", "polyclinic"]
# }


# Prepare a lower-case version of the dictionary for case-insensitive comparison
generalizations_lower = {k: [word.lower() for word in v] for k, v in generalizations_nigeria.items()}

source_field = "g3_hltfac_type"
target_field = "g3_hltfac_type_generalized"

# Check and add the target field if it doesn't exist
fields = [f.name for f in arcpy.ListFields(feature_class)]
if target_field not in fields:
    arcpy.AddField_management(feature_class, target_field, "TEXT")

# Use an update cursor to iterate through the feature class
with arcpy.da.UpdateCursor(feature_class, [source_field, target_field]) as cursor:
    for row in cursor:
        # # uncomment to skip the update if the target field already has data 
        # if row[1]: 
        #     continue

        source_value_lower = row[0].lower() if row[0] else "" 
        match_found = False
        
        for generalized, keywords in generalizations_lower.items():
            for keyword in keywords:
                if keyword in source_value_lower:
                    # Assign the generalized category (capitalize the key)
                    row[1] = generalized.capitalize()
                    cursor.updateRow(row)
                    match_found = True
                    break  # Stop checking this row once a match is found
            if match_found:
                break
        
        # If no keywords matched, assign "Other" to the target field
        if not match_found:
            row[1] = "Other"
            cursor.updateRow(row)

print("done.")