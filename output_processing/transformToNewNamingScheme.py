import os
import re

def transform_filename(old_name):
    """
    Transform a filename from the old pattern to the new pattern.

    Old pattern: 
    pageSize_CountryAdmin_ProvinceAdmin_AntenneAdmin_ZoneSanteAdmin_AireSanteAdmin_uniquePage_useCase_dateYYYYMMDD.jpg

    New pattern:
    pageSize_useCase_CountryAdmin_ProvinceAdmin_AntenneAdmin_ZoneSanteAdmin_AireSanteAdmin_uniquePage_dateYYYYMMDD.jpg
    """
    # Regex to capture the components of the old filename
    match = re.match(
        r"^(.*?)_(.*?)_(.*?)_(.*?)_(.*?)_(.*?)_(.*?)_(\d{8})(?:_(\d+))?(?:\.jpg|\.pdf)$", old_name
    )

    if not match:
        print(f"Filename does not match the expected pattern: {old_name}")
        return None

    # Extract components
    pageSize, country, province, antenne, healthzone, healtharea, usecase, date, sequential = match.groups()

    # Default the sequential number to "1" if it's missing
    sequential = sequential if sequential else "1"

    # Construct the new filename
    new_name = (
        f"{pageSize}_{usecase}_{country}_{province}_{antenne}_{healthzone}_{healtharea}_"
        f"{sequential}_{date}.jpg"
    )

    return new_name

def rename_files_in_directory(directory):
    """Rename files in the directory based on the new naming convention."""
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.pdf')):
            new_name = transform_filename(filename)
            if new_name:
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_name)

                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {filename} -> {new_name}")
                except Exception as e:
                    print(f"Error renaming {filename} to {new_name}: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Rename files to a new naming convention.")
    parser.add_argument("directory", type=str, help="Path to the directory containing files to rename.")
    args = parser.parse_args()

    rename_files_in_directory(args.directory)
