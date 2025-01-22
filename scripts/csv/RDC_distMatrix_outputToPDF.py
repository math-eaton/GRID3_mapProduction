import os
import pandas as pd
from weasyprint import HTML

def clean_text(text):
    cleaned_text = ''.join(i for i in text if ord(i) < 128).replace(' ', '-')
    cleaned_text = cleaned_text.replace('/', '-').replace('\\', '-').replace("'", '')
    return cleaned_text.replace('---', '-')

def format_dataframe(df):
    html = df.to_html(index=False, justify='right')
    return html

def save_html_to_pdf(html_content, output_pdf_path):
    HTML(string=html_content).write_pdf(output_pdf_path)

def rename_and_format_files(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(input_directory, filename)
            try:
                df = pd.read_excel(file_path, engine='openpyxl')
                if 'pageName' in df.columns:
                    page_name = df['pageName'].iloc[0]
                    cleaned_page_name = clean_text(page_name)
                    new_filename_base = f"RDC_Maniema_{cleaned_page_name}"
                    new_filename = new_filename_base + '.xlsx'
                    new_file_path = os.path.join(input_directory, new_filename)

                    os.rename(file_path, new_file_path)

                    html_content = format_dataframe(df)
                    page_num = 1
                    output_pdf_path = os.path.join(output_directory, f"{new_filename_base}_{page_num}.pdf")
                    save_html_to_pdf(html_content, output_pdf_path)
                    page_num += 1

                    print(f"Formatted and saved {new_filename_base} to {output_pdf_path}")

            except Exception as e:
                print(f"Error processing file {filename}: {e}")

# Usage
input_directory = '/Users/matthewheaton/Downloads/maniemaoptimizedlocationscatchments/distance_matrix_by_AS'
output_directory = '/Users/matthewheaton/Downloads/maniemaoptimizedlocationscatchments/distMatrix_AS_formatted'
rename_and_format_files(input_directory, output_directory)
