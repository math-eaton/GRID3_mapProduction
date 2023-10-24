import os

directory = r'/Users/matthewheaton/Downloads/maps_20231020/optimized'

# Check if directory exists
if not os.path.exists(directory):
    print(f"Directory '{directory}' does not exist!")
    exit()

# Print all filenames
print("Files in the directory:")
for filename in os.listdir(directory):
    print(filename)

# Iterate through all files in the directory
for filename in os.listdir(directory):
    full_path = os.path.join(directory, filename)

    # Ensure it's a file
    if os.path.isfile(full_path):
        # Convert filename to title case for comparison
        title_filename = filename.title()

        # Check if the title-cased filename contains "A0_Province_"
        if "A0_Province_" in title_filename:
            # Replace "a0_province_" with "a3_landscape_" in the original filename
            new_filename = filename.replace("a0_province_", "a3_landscape_")
            new_full_path = os.path.join(directory, new_filename)

            # Rename the file
            try:
                os.rename(full_path, new_full_path)
                print(f"Renamed: '{filename}' to '{new_filename}'")
            except Exception as e:
                print(f"Error renaming '{filename}': {e}")

print("Renaming done.")
