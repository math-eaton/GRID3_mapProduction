import os
import pandas as pd
from collections import defaultdict
from datetime import datetime
import argparse
import shutil

def parse_filename(filename):
    """Parse the filename into components based on underscores."""
    parts = filename.split('_')
    if len(parts) < 9:
        return None  # Invalid filename structure

    return {
        'PageSize': parts[0],
        'UseCase': parts[1],
        'Admin0Country': parts[2],
        'Admin1Province': parts[3],
        'Admin2Antenne': parts[4],
        'Admin3ZoneSante': parts[5],
        'Admin4AireSante': parts[6],
        'UniquePageSequential': parts[7],
        'Date': parts[8].split('.')[0],  # Remove extension
    }

def summarize_directory(directory):
    """Generate a flexible hierarchical summary."""
    # Define the hierarchy as individual keys
    hierarchy = [
        "PageSize",
        "UseCase",
        "Admin0Country",
        "Admin1Province",
        "Admin2Antenne",
        "Admin3ZoneSante",
        "Admin4AireSante",
        "UniquePageSequential",
    ]

    data = defaultdict(lambda: defaultdict(set))
    for filename in os.listdir(directory):
        if not filename.endswith(('.jpg', '.pdf')):
            continue

        parsed = parse_filename(filename)
        if not parsed:
            continue

        # Build progressive keys for hierarchy dynamically
        for i in range(len(hierarchy)):
            key = "_".join(parsed[h] for h in hierarchy[:i + 1])
            data["_".join(hierarchy[:i + 1])][key].add(filename)

    # Build summary report
    rows = []
    for level in data.keys():
        # Skip the "UniquePageSequential" level
        if level == "PageSize_UseCase_Admin0Country_Admin1Province_Admin2Antenne_Admin3ZoneSante_Admin4AireSante_UniquePageSequential":
            continue

        for key, files in data[level].items():
            # Check for multipart polygons at the desired level
            if level == "PageSize_UseCase_Admin0Country_Admin1Province_Admin2Antenne_Admin3ZoneSante_Admin4AireSante":
                multipart = len(files) > 1
            else:
                multipart = False

            rows.append({
                "Level": level,
                "Key": key,
                "UniqueCount": len(files),
                "MULTIPART": multipart,
            })

    return pd.DataFrame(rows)

def save_summary_to_excel_sheets(summary_df, output_file):
    """Save the summary DataFrame into multiple sheets of an Excel file."""
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        # Iterate through unique levels in reverse order (most specific to least specific)
        unique_levels = sorted(summary_df["Level"].unique(), reverse=True)
        for level in unique_levels:
            # Filter rows for the current level
            level_df = summary_df[summary_df["Level"] == level]
            # Extract the last part of the level key for the sheet name
            sheet_name = level.split("_")[-1]
            # Write to the Excel sheet
            level_df.to_excel(writer, index=False, sheet_name=sheet_name[:31])  # Sheet name max length = 31

    print(f"Excel file saved with sheets: {output_file}")


def organize_files_by_hierarchy(directory, organize=True):
    """Organize files into nested subdirectories based on their qualities and admin units."""
    if not organize:
        print("File organization skipped.")
        return

    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.pdf')):
            parsed = parse_filename(filename)
            if not parsed:
                continue

            # Create a directory structure
            components = [
                parsed['Admin0Country'],
                parsed['Admin1Province'],
                parsed['Admin2Antenne'],
                parsed['Admin3ZoneSante'],
                parsed['Admin4AireSante'],
            ]
            target_directory = os.path.join(directory, *components)
            os.makedirs(target_directory, exist_ok=True)

            # Move the file to the target directory
            source_path = os.path.join(directory, filename)
            destination_path = os.path.join(target_directory, filename)
            try:
                shutil.move(source_path, destination_path)
            except Exception as e:
                print(f"Error moving file {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize and organize files in a directory.")
    parser.add_argument('input_directory', type=str, help="Path to the input directory.")
    parser.add_argument('--organize', action='store_true', help="Whether to organize files into subdirectories.")
    args = parser.parse_args()

    input_directory = args.input_directory
    organize_files = args.organize

    # Determine output file name
    directory_name = os.path.basename(os.path.normpath(input_directory))
    date_suffix = datetime.now().strftime("%Y%m%d")
    excel_output = os.path.join(input_directory, f"{directory_name}_report_{date_suffix}.xlsx")

    # Summarize directory
    summary_df = summarize_directory(input_directory)

    # Save summary to Excel with multiple sheets
    save_summary_to_excel_sheets(summary_df, excel_output)

    # Optional: Organize files into nested subdirectories
    if organize_files:
        organize_files_by_hierarchy(input_directory, organize=True)

    print("Summary saved to:")
    print(f"Excel: {excel_output}")
    if organize_files:
        print("Files organized into nested directories.")