import pandas as pd
import os

def extract_information_from_path(file_path):
    # Extract State, LGA, and Ward from the file path
    path_parts = file_path.split(os.sep)
    state = path_parts[-4]
    lga = path_parts[-3]
    ward = path_parts[-2]

    # Read all sheets in the Excel file
    sheets = pd.read_excel(file_path, sheet_name=None, header=None)

    # List to store the extracted information
    data_list = []

    # Iterate over each sheet
    for sheet_name, sheet_df in sheets.items():
        # Extract the Name of Health Facility/Take-off Point from cell E2 (using index positions)
        takeoff_hp = sheet_df.iat[1, 4]  # 1st row (index 1), 5th column (index 4)

        # Iterate through the column indexes for B through J (1 to 9)
        for col_index in range(1, 10):
            # Extract the required information from the specified cells using index positions
            vp_location = sheet_df.iat[10, col_index]  # 11th row, column index
            settlement_name = sheet_df.iat[11, col_index]  # 12th row, column index
            distance_hp_to_vp = sheet_df.iat[13, col_index]  # 14th row, column index

            # Check if the VP location is not empty
            if pd.notna(vp_location):
                # Add the extracted information to the list
                data_list.append({
                    "State": state,
                    "LGA": lga,
                    "Ward": ward,
                    "Takeoff HP": takeoff_hp,
                    "VP location": vp_location,
                    "Settlement name": settlement_name,
                    "Distance HP to VP": distance_hp_to_vp
                })

    # Convert the list to a DataFrame
    extracted_data = pd.DataFrame(data_list, columns=["State", "LGA", "Ward", "Takeoff HP", 
                                                      "VP location", "Settlement name", "Distance HP to VP"])

    # Save the extracted information to a new Excel file
    extracted_data.to_excel("processing/NGA_KanoDIP/output/sample.xlsx", index=False)

# Usage
file_path = '/Users/matthewheaton/Documents/GitHub/GRID3_mapProduction/processing/NGA_KanoDIP/Kano/Dambatta LGA/Ajumawa/Measles DIP Ajumawa.xlsx'  # Replace with the full path to your Excel file
extract_information_from_path(file_path)