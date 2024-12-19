import os
import shutil
import pandas as pd
from collections import defaultdict

def parse_filename(filename):
    """Parse the filename into components based on underscores."""
    parts = filename.split('_')
    if len(parts) < 8:
        return None  # Invalid filename

    return {
        'pageSize': parts[0],
        'country': parts[1],
        'province': parts[2],
        'antenne': parts[3],
        'zoneSante': parts[4],
        'aireSante': parts[5],
        'uniquePage': parts[6],
        'useCase': parts[7],
        'date': parts[8].split('.')[0],
    }

def summarize_directory(directory):
    """Summarize the contents of a directory based on file names."""
    summary = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int)))))

    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.pdf')):
            parsed = parse_filename(filename)
            if not parsed:
                continue

            # Increment counts for each level
            useCase = parsed['useCase']
            country = parsed['country']
            province = parsed['province']
            antenne = parsed['antenne']
            zoneSante = parsed['zoneSante']
            aireSante = parsed['aireSante']

            summary[useCase][country][province][antenne][zoneSante] += 1

    return summary

def generate_summary_table(summary):
    """Generate a summary table from the nested summary dictionary."""
    rows = []

    for useCase, countries in summary.items():
        for country, provinces in countries.items():
            for province, antennes in provinces.items():
                for antenne, zones in antennes.items():
                    for zoneSante, count in zones.items():
                        rows.append({
                            'useCase_nom': useCase,
                            'useCase_count': sum(zones.values()),
                            'country_nom': country,
                            'country_count': sum(sum(zone.values()) for zone in antennes.values()),
                            'province_nom': province,
                            'province_count': sum(zone.values() for zone in antennes[antenne].values()),
                            'antenne_nom': antenne,
                            'antenne_count': sum(zones.values()),
                            'zoneSante_nom': zoneSante,
                            'zoneSante_count': count,
                        })

    return pd.DataFrame(rows)

def save_summary_to_excel(df, output_file):
    """Save the summary DataFrame to an Excel file."""
    df.to_excel(output_file, index=False)

def save_summary_to_csv(df, output_file):
    """Save the summary DataFrame to a CSV file."""
    df.to_csv(output_file, index=False)

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

            province = parsed['province']
            useCase = parsed['useCase']
            antenne = parsed['antenne']
            zoneSante = parsed['zoneSante']
            aireSante = parsed['aireSante']

            # Create the nested directory structure
            target_directory = os.path.join(directory, province, useCase, antenne, zoneSante, aireSante)
            os.makedirs(target_directory, exist_ok=True)

            # Move the file to the target directory
            source_path = os.path.join(directory, filename)
            destination_path = os.path.join(target_directory, filename)
            try:
                shutil.move(source_path, destination_path)
            except Exception as e:
                print(f"Error moving file {filename}: {e}")

if __name__ == "__main__":
    # Input directory containing the map files
    input_directory = "path/to/your/directory"

    # Output files
    excel_output = "map_summary.xlsx"
    csv_output = "map_summary.csv"

    # Option to organize files
    organize_files = True

    # Summarize directory
    summary = summarize_directory(input_directory)

    # Generate summary table
    summary_df = generate_summary_table(summary)

    # Save summary to Excel and CSV
    save_summary_to_excel(summary_df, excel_output)
    save_summary_to_csv(summary_df, csv_output)

    # Organize files into nested subdirectories
    organize_files_by_hierarchy(input_directory, organize=organize_files)

    print("Summary saved to:")
    print(f"Excel: {excel_output}")
    print(f"CSV: {csv_output}")
    if organize_files:
        print("Files organized into nested directories.")
