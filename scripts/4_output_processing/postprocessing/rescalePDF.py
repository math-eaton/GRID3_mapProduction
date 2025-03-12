import fitz  # PyMuPDF
import os

def resize_pdf(input_dir, output_dir, original_dpi, target_dpi):
    scale_factor = target_dpi / original_dpi

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # Open the PDF
            doc = fitz.open(input_path)

            # Iterate through each page
            for page in doc:
                # Get the current page size
                rect = page.rect
                new_rect = fitz.Rect(rect.tl, rect.br * scale_factor)
                page.set_cropbox(new_rect)

            # Save the resized PDF
            doc.save(output_path)
            doc.close()

input_directory = "path/to/input/folder"
output_directory = "path/to/output/folder"
original_dpi = 1200  # original DPI
target_dpi = 300  # target DPI

resize_pdf(input_directory, output_directory, original_dpi, target_dpi)
