import os
import time
from pdf2image import convert_from_path
from PIL import Image

def convert_pdf_to_jpg(pdf_path, output_path, dpi=300, quality=85):
    """
    Convert a PDF file into optimized JPG images and save them to the specified output path.
    
    :param pdf_path: Path to the PDF file.
    :param output_path: Path where the JPG images will be saved.
    :param dpi: DPI for conversion, affects the resolution. Default is 300.
    :param quality: Quality of the output JPG images, 1-100. Default is 85.
    """
    images = convert_from_path(pdf_path, dpi=dpi)
    for i, image in enumerate(images):
        image_file_path = f"{output_path}_page_{i+1}.jpg"
        image.save(image_file_path, 'JPEG', quality=quality, optimize=True)
        print(f"Saved: {image_file_path}")

def process_directory(input_directory, output_directory, dpi=300, quality=85, limit=5):
    """
    Recursively process all PDF files in the input directory, converting them to JPG,
    and replicating the directory structure in the output directory.

    :param input_directory: The input directory to search for PDF files.
    :param output_directory: The output directory to save JPG images.
    :param dpi: DPI for conversion. Default is 300.
    :param quality: Quality of the output JPG images. Default is 85.
    :param limit: Optional limit on the number of files to process for testing. Default is 5.
    """
    file_count = 0
    start_time = time.time()

    for root, dirs, files in os.walk(input_directory):
        relative_path = os.path.relpath(root, input_directory)
        output_root = os.path.join(output_directory, relative_path)
        
        if not os.path.exists(output_root):
            os.makedirs(output_root)

        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                output_path = os.path.join(output_root, os.path.splitext(file)[0])

                file_start_time = time.time()
                convert_pdf_to_jpg(pdf_path, output_path, dpi=dpi, quality=quality)
                file_end_time = time.time()

                print(f"Processed {pdf_path} in {file_end_time - file_start_time:.2f} seconds.")
                file_count += 1

                if file_count == limit:
                    break

        if file_count == limit:
            break

    total_time = time.time() - start_time
    print(f"Processed {file_count} files in {total_time:.2f} seconds.")


# Define your input and output directories
input_directory = r'D:\GRID\NGA\map_production\NGA_Gombe-Ogun_202402\microplanning_projects\OUTPUT_A1_microplanning_20240313'
output_root = r'D:\GRID\NGA\map_production\NGA_Gombe-Ogun_202402\microplanning_projects\OUTPUT_A1_microplanning_JPG_20240314'
