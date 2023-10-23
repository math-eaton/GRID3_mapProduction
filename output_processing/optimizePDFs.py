import fitz  # PyMuPDF
import os

def optimize_pdf(input_path, output_path):
    try:
        pdf_document = fitz.open(input_path)
        pdf_document.save(output_path, garbage=4, deflate=True)
        pdf_document.close()
        print(f"Optimization complete. Saved as {output_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def optimize_pdfs_in_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            optimize_pdf(input_path, output_path)

if __name__ == "__main__":
    input_directory = "/Users/matthewheaton/Downloads/maps_20231020"  # replace with input directory path
    output_directory = "/Users/matthewheaton/Downloads/maps_20231020/optimized"  # replace with output directory path

    optimize_pdfs_in_directory(input_directory, output_directory)
