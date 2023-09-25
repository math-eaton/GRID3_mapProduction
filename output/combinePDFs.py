import os
from PyPDF2 import PdfFileMerger

# Get the current directory
current_directory = os.getcwd()

# Create a list to store the PDF file paths
pdf_files = []

# Iterate through all files in the directory
for filename in os.listdir(current_directory):
    if filename.lower().endswith('.pdf'):
        pdf_files.append(os.path.join(current_directory, filename))

# Sort the PDF files
pdf_files.sort(key=str.lower)

# Create a PdfFileMerger object
pdf_merger = PdfFileMerger()

# Append each PDF to the merger object
for pdf_file in pdf_files:
    pdf_merger.append(pdf_file)

# Define the output PDF file name (same as the directory name)
output_pdf_name = os.path.basename(current_directory) + '.pdf'

# Write the merged PDF to the output file
with open(output_pdf_name, 'wb') as output_pdf:
    pdf_merger.write(output_pdf)

# Close the merger object
pdf_merger.close()

print(f'Merged PDF saved as {output_pdf_name}')
