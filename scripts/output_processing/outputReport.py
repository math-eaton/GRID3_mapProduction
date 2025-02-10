import os
import pandas as pd
from collections import defaultdict
from datetime import datetime
import argparse
import shutil
import random

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

def save_summary_to_excel_sheets(summary_df, output_file, input_directory):
    """Save the summary DataFrame into multiple sheets of an Excel file and add a QA_QC sheet."""
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

        # Generate QA_QC sheet
        qa_qc_data = generate_qa_qc_data(input_directory)
        qa_qc_df = pd.DataFrame({"check": qa_qc_data})
        qa_qc_df.to_excel(writer, index=False, sheet_name="QA_QC")

def generate_qa_qc_data(directory, copy_to_check=True):
    """Generate a list of random filenames for each unique Admin3ZoneSante level and optionally copy them."""
    qa_qc_data = []
    file_map = defaultdict(list)

    # Collect filenames under each [-4] component (Admin3ZoneSante level)
    for filename in os.listdir(directory):
        if not filename.endswith(('.jpg', '.pdf')):
            continue

        # Extract the [-4] component from the filename
        components = filename.split('_')
        if len(components) < 5:  # Ensure filename has enough parts
            continue
        admin3_key = components[-4]  # Extract the fourth-to-last part
        file_map[admin3_key].append(filename)

    # Select one random file per Admin3ZoneSante
    check_dir = os.path.join(directory, "0_check")
    if copy_to_check:
        os.makedirs(check_dir, exist_ok=True)  # Ensure the "check" directory exists

    for admin3, files in file_map.items():
        selected_file = random.choice(files)
        qa_qc_data.append(selected_file)

        # Optionally copy the file to the "check" subdirectory
        if copy_to_check:
            src_path = os.path.join(directory, selected_file)
            dst_path = os.path.join(check_dir, selected_file)
            try:
                shutil.copy(src_path, dst_path)
            except Exception as e:
                print(f"Error copying file {selected_file}: {e}")

    return qa_qc_data

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

    # Save summary to Excel with multiple sheets and QA_QC
    save_summary_to_excel_sheets(summary_df, excel_output, input_directory)

    # Optional: Organize files into nested subdirectories
    if organize_files:
        organize_files_by_hierarchy(input_directory, organize=True)

    print("Summary saved to:")
    print(f"Excel: {excel_output}")
    if organize_files:
        print("Files organized into nested directories.")
