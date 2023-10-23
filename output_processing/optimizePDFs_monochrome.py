import subprocess
import os

os.environ["PATH"] += os.pathsep + "/usr/local/bin"


def optimize_with_ghostscript(input_path, output_path, dpi=250):
    """
    Use Ghostscript to reduce the size of a monochromatic PDF for printing.
    
    :param input_path: Path to the input PDF.
    :param output_path: Path to save the optimized PDF.
    :param dpi: Desired resolution for the output. Adjust based on quality needs.
    """
    # Core Ghostscript parameters
    gs_command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/printer",
        "-dDetectDuplicateImages=true",
        f"-r{dpi}",
        "-dColorConversionStrategy=/Gray",
        "-dProcessColorModel=/DeviceGray",
        "-dAutoFilterGrayImages=false",
        f"-dGrayImageResolution={dpi}",
        f"-sOutputFile={output_path}",
        input_path
    ]
    
    try:
        subprocess.run(gs_command, check=True)
        print(f"Optimization complete. Saved as {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Ghostscript command failed with error: {str(e)}")


def optimize_pdfs_in_directory(input_dir):
    output_dir = os.path.join(input_dir, "optimized")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            # creating the new filename with the "_mono-optimized" suffix
            base_name = os.path.splitext(filename)[0]
            new_filename = f"{base_name}_mono-optimized.pdf"
            output_path = os.path.join(output_dir, new_filename)
            optimize_with_ghostscript(input_path, output_path)


if __name__ == "__main__":
    input_directory = "/Users/matthewheaton/Downloads/maps_20231020"  # replace with your directory path
    optimize_pdfs_in_directory(input_directory)
