import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook

# Function to install required packages
def install_packages():
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "openpyxl", "matplotlib"])

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    from openpyxl import load_workbook
except ImportError:
    install_packages()

def process_excel_files(directory, max_files=None):
    count = 0

    output_dir = os.path.join(directory, 'table_img')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(directory):
        if "_km" in filename.lower() and filename.endswith('.xlsx'):
            if max_files is not None and count >= max_files:
                break
            filepath = os.path.join(directory, filename)
            # Process the filename to create a valid output image name
            base_name = filename.split('_')[0]
            safe_name = re.sub(r"[ ']", lambda x: '-' if x.group() == ' ' else '', base_name)
            output_filename = f"{safe_name}.jpg"

            # Read the Excel file
            wb = load_workbook(filepath, data_only=True)
            ws = wb.active

            # Collect data from the sheet
            data = []
            for row in ws.iter_rows(values_only=True):
                if any(cell is not None for cell in row):  # Check if there are any non-null cells
                    data.append(row)

            # Convert data to DataFrame
            df = pd.DataFrame(data)

            # Plotting the DataFrame
            fig, ax = plt.subplots(figsize=(8, 6))  # You can adjust figsize to better fit your data
            ax.axis('tight')
            ax.axis('off')
            table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colColours=["#f2f2f2"]*df.shape[1])
            table.auto_set_font_size(False)
            table.set_fontsize(12)
            table.scale(1.2, 1.2)  # Adjust scale to fit the figure better

            # Apply bold font to the header
            for (i, col), cell in table.get_celld().items():
                if i == 0:
                    cell.get_text().set_weight('bold')
                    cell.get_text().set_fontsize(12)
                    cell.get_text().set_family('Arial')

            output_filename = os.path.join(output_dir, f"{safe_name}.jpg")
            plt.savefig(output_filename, dpi=300, pil_kwargs={'quality': 80})
            plt.close()

            print(f"Saved image as {output_filename}")
            count += 1

# params
directory = "E:\mheaton\cartography\COD_microplanning_042024\data\input\distance_matrix_by_AS"
process_excel_files(directory, max_files=5)
