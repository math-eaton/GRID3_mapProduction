import arcpy
import csv

# Update the path to your input geodatabase
arcpy.env.workspace = r'E:\mheaton\cartography\NGA_microplanning_2024\data\processing\Ogun_NMEP_maps_layers_processing_COPY.gdb'

# Update the path to your CSV containing translations
csv_path = r'E:\mheaton\cartography\NGA_microplanning_2024\NGA_abbreviationDict.csv'

# Fields to check for translations
target_fields = ['health_facility', 'distribution_hub', 'dh_name_clean']

# Load translations from CSV into a dictionary
translation_dict = {}
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        # Store translations with lower case keys for case insensitive matching
        translation_dict[row[0].lower()] = row[1]

# Function to apply translations
def apply_translations(feature_class, fields):
    # Sort the dictionary by key length in descending order to match longer phrases first
    sorted_translations = sorted(translation_dict.items(), key=lambda x: -len(x[0]))
    # Iterate over each target field
    for field in fields:
        if field in [f.name for f in arcpy.ListFields(feature_class)]:
            print(f"Applying translations to field '{field}' in {feature_class}...")
            with arcpy.da.UpdateCursor(feature_class, field) as cursor:
                for row in cursor:
                    original_value = row[0]
                    if original_value:
                        # Make the comparison case-insensitive
                        lower_value = original_value.lower()
                        for key, translation in sorted_translations:
                            if key in lower_value:
                                # Replace and maintain the original case of the first character
                                row[0] = lower_value.replace(key, translation)
                                row[0] = row[0][0].upper() + row[0][1:]
                                cursor.updateRow(row)
                                break  # Stop after the first successful translation

# List of feature classes to process
feature_classes = arcpy.ListFeatureClasses()

# Process each feature class
for feature_class in feature_classes:
    print(f"Processing {feature_class}...")
    apply_translations(feature_class, target_fields)

print("Processing completed.")
