import subprocess
import os
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

os.environ["PATH"] += os.pathsep + "/usr/local/bin"

def optimize_with_ghostscript(input_path, output_path, dpi=250, mode="GRAY"):
    """
    Optimize PDF using Ghostscript.

    Modes:
    - "GRAY": Monochrome Grayscale processing
    - "CMYK": Full-color CMYK processing
    """
    # Common Ghostscript parameters
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
        f"-sOutputFile={output_path}",
        input_path
    ]

    # Adjusting parameters based on mode
    if mode == "GRAY":
        gs_command.extend([
            "-dColorConversionStrategy=/Gray",
            "-dProcessColorModel=/DeviceGray",
            "-dAutoFilterGrayImages=false",
            f"-dGrayImageResolution={dpi}"
        ])
    elif mode == "CMYK":
        gs_command.extend([
            "-dProcessColorModel=/DeviceCMYK",
            "-dAutoFilterColorImages=false",
            f"-dColorImageResolution={dpi}"
        ])
    else:
        raise ValueError("Invalid mode. Choose either 'GRAY' or 'CMYK'.")

    try:
        subprocess.run(gs_command, check=True)
        print(f"Optimization complete. Saved as {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Ghostscript command failed with error: {str(e)}")


def worker(filename, input_dir, mode):
    input_path = os.path.join(input_dir, filename)
    base_name = os.path.splitext(filename)[0]
    new_filename = f"{base_name}_optimized.pdf"
    output_dir = os.path.join(input_dir, "optimized")
    output_path = os.path.join(output_dir, new_filename)
    optimize_with_ghostscript(input_path, output_path, mode=mode)

def optimize_pdfs_in_directory(input_dir, mode="GRAY", max_workers=None):
    output_dir = os.path.join(input_dir, "optimized")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filenames = [filename for filename in os.listdir(input_dir) if filename.endswith(".pdf")]
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        list(tqdm(executor.map(worker, filenames, [input_dir]*len(filenames), [mode]*len(filenames)), total=len(filenames), desc="Optimizing PDFs"))

if __name__ == "__main__":
    input_directory = "/Users/matthewheaton/Downloads/maps_20231020"  # replace with your directory path
    mode_to_use = "CMYK"  # Change to "GRAY" for grayscale
    optimize_pdfs_in_directory(input_directory, mode=mode_to_use, max_workers=4)  # Adjust max_workers based on the number of available CPU cores
