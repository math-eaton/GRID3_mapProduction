import os
import pandas as pd

def clean_text(text):
    # Remove non-ascii characters and replace spaces with hyphens
    cleaned_text = ''.join(i for i in text if ord(i) < 128).replace(' ', '-')
    # Replace forward/backslashes, apostrophes, and ensure triple hyphens are reduced to single
    cleaned_text = cleaned_text.replace('/', '-').replace('\\', '-').replace("'", '')
    return cleaned_text.replace('---', '-')

def rename_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(directory, filename)
            try:
                df = pd.read_excel(file_path, engine='openpyxl')
                if 'pageName' in df.columns:
                    page_name = df['pageName'].iloc[0]
                    cleaned_page_name = clean_text(page_name)
                    new_filename = f"RDC_Maniema_{cleaned_page_name}.xlsx"
                    new_file_path = os.path.join(directory, new_filename)
                    os.rename(file_path, new_file_path)
                    print(f"Renamed {filename} to {new_filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")


# Usage
input_directory = '/Users/matthewheaton/Downloads/maniemaoptimizedlocationscatchments/distance_matrix_by_AS'
rename_files(input_directory)
