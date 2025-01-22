import os
import glob
import pandas as pd
import arcpy

# Directory containing PDFs
pdf_directory = 'path_to_your_pdf_directory'
# Path to your map series index polygon feature class
feature_class_path = 'path_to_feature_class'

# check if the number of PDFs matches the number of records in the feature class
def check_pdf_count():
    pdf_files = glob.glob(os.path.join(pdf_directory, '*.pdf'))
    pdf_count = len(pdf_files)
    
    # access the feature class and count its records
    feature_class_count = int(arcpy.GetCount_management(feature_class_path).getOutput(0))
    
    return pdf_count == feature_class_count

# check for outliers in file size
def check_file_size_outliers(threshold=2.0):
    pdf_files = glob.glob(os.path.join(pdf_directory, '*.pdf'))
    file_size_data = []
    
    for pdf_file in pdf_files:
        file_size = os.path.getsize(pdf_file) / (1024 * 1024)  # Convert to MB
        file_size_data.append((os.path.basename(pdf_file), file_size))
    
    df = pd.DataFrame(file_size_data, columns=['File Name', 'File Size (MB)'])
    mean_size = df['File Size (MB)'].mean()
    std_dev = df['File Size (MB)'].std()
    
    # Identify files with size more than (mean + threshold * std deviation)
    outliers = df[df['File Size (MB)'] > (mean_size + threshold * std_dev)]
    
    return outliers

##################

# Generate the HTML or Markdown report
def generate_report():
    pdf_count_check = check_pdf_count()
    file_size_outliers = check_file_size_outliers()
    
    # Create an HTML or Markdown report
    report = ""
    
    report += "# QA/QC Overview\n\n"
    
    if pdf_count_check:
        report += "## PDF Count Check\n"
        report += "The number of PDF output files matches the number of records in the feature class.\n\n"
    else:
        report += "## PDF Count Check (Error)\n"
        report += "The number of PDF output files does not match the number of records in the feature class.\n\n"
    
    if not file_size_outliers.empty:
        report += "## File Size Outliers (Potential Encoding Errors)\n"
        report += "The following PDF files have file sizes significantly larger than the mean size, which may indicate encoding errors:\n\n"
        report += file_size_outliers.to_html(index=False)
    else:
        report += "## File Size Outliers\n"
        report += "No file size outliers detected.\n\n"
    
###########
    
    # save the report to html file (alternatively save as md)
    with open('qa_qc_report.html', 'w') as f:
        f.write(report)

if __name__ == "__main__":
    generate_report()