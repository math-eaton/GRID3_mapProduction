import os

directory = r'E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\OUTPUT_A2_reference_x_20241215'

# Check if directory exists
if not os.path.exists(directory):
    print(f"Directory '{directory}' does not exist!")
    exit()

# Print all filenames
# print("Files in the directory:")
# for filename in os.listdir(directory):
    # print(filename)

# Iterate through all files in the directory
for filename in os.listdir(directory):
    full_path = os.path.join(directory, filename)

    # Ensure it's a file
    if os.path.isfile(full_path):
        # Convert filename to title case for comparison
        # title_filename = filename.title()
        title_filename = filename
        print(title_filename)

        # Check if the title-cased filename contains "xyz"
        if "A2" in title_filename:
            # Replace "X"[0] with "Y"[1] in the original filename 
            new_filename = filename.replace("reference_x", "reference")
            new_full_path = os.path.join(directory, new_filename)

            # Rename the file
            try:
                os.rename(full_path, new_full_path)
                # print(f"Renamed: '{filename}' to '{new_filename}'")
            except Exception as e:
                print(f"Error renaming '{filename}': {e}")

print("Renaming done.")
