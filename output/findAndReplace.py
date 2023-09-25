import os

directory = r'D:\xyz'

# Iterate through all files in the directory
for filename in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, filename)):
        # Check if the filename contains "North-Weatern"
        if "North-Weatern" in filename:
            # Replace "North-Weatern" with "North-Western" in the filename
            new_filename = filename.replace("North-Weatern", "North-Western")
            # Rename the file
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

print("File renaming complete.")
