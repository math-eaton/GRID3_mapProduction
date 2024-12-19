import arcpy
import os

# Set the workspace to the folder containing the Excel files
excel_directory = r"\\devgriarc0\DdriveDevgriarc0\data\nga\microplans\P3b_malaria_microplans\Ogun_2024\distribution_hubs\toJoin_20241007"
# Define the output geodatabase where the tables will be saved
output_gdb = r"\\devgriarc0\DdriveDevgriarc0\data\nga\microplans\P3b_malaria_microplans\Ogun_2024\distribution_hubs\toJoin_20241007\toJoin_20241007.gdb"

# Iterate through all files in the directory
for filename in os.listdir(excel_directory):
    # Check if the file is an Excel file (.xls or .xlsx)
    if filename.endswith('.xls') or filename.endswith('.xlsx'):
        excel_file = os.path.join(excel_directory, filename)

        print(f"converting {filename}...")
        
        # Define the name of the output table
        table_name = os.path.splitext(filename)[0]  # Remove the file extension
        output_table = os.path.join(output_gdb, table_name)
        
        # Run the Excel to Table tool
        try:
            arcpy.ExcelToTable_conversion(excel_file, output_table)
            print(f"Successfully converted {filename} to {output_table}")
        except arcpy.ExecuteError:
            print(f"Error converting {filename}: {arcpy.GetMessages()}")

print("All Excel files processed.")
