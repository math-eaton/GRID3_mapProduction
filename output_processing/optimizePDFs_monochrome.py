import subprocess
import os
from concurrent.futures import ProcessPoolExecutor

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


def worker(filename, input_dir):
    """This will be our worker function to be used by each process in the pool."""
    input_path = os.path.join(input_dir, filename)
    base_name = os.path.splitext(filename)[0]
    new_filename = f"{base_name}_mono-optimized.pdf"
    output_dir = os.path.join(input_dir, "optimized")
    output_path = os.path.join(output_dir, new_filename)
    optimize_with_ghostscript(input_path, output_path)

def optimize_pdfs_in_directory(input_dir, max_workers=None):
    output_dir = os.path.join(input_dir, "optimized")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filenames = [filename for filename in os.listdir(input_dir) if filename.endswith(".pdf")]
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # use the executor to map the worker function over all filenames
        list(executor.map(worker, filenames, [input_dir]*len(filenames)))

if __name__ == "__main__":
    input_directory = "/Users/matthewheaton/Downloads/maps_20231020"  # replace with your directory path
    optimize_pdfs_in_directory(input_directory, max_workers=4)  # Adjust max_workers based on the number of available CPU cores
