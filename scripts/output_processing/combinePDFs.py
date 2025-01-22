import os
from PyPDF2 import PdfFileMerger

# Define the input directory
input_directory = r'D:\inputDirPath'

# Iterate through all subdirectories and their files
for root, dirs, files in os.walk(input_directory):
    # Create a list to store the PDF file paths for the current subdirectory
    pdf_files = []

    # Iterate through files in the current subdirectory
    for filename in files:
        if filename.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(root, filename))

    # Sort the PDF files within the subdirectory
    pdf_files.sort(key=str.lower)

    # Check if there are any PDF files in the subdirectory
    if pdf_files:
        # Create a PdfFileMerger object
        pdf_merger = PdfFileMerger()

        # Append each PDF to the merger object
        for pdf_file in pdf_files:
            pdf_merger.append(pdf_file)

        # Define the output PDF file name based on the subdirectory name
        subdirectory_name = os.path.basename(root)
        output_pdf_name = os.path.join(root, subdirectory_name + '.pdf')

        # Write the merged PDF to the output file
        with open(output_pdf_name, 'wb') as output_pdf:
            pdf_merger.write(output_pdf)

        # Close the merger object
        pdf_merger.close()

        print(f'Merged PDFs in "{subdirectory_name}" and saved as "{output_pdf_name}"')

print('all PDFs merged.')
