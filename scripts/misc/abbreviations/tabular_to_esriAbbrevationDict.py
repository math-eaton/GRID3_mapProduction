import pandas as pd

# Load the Excel file
file_path = 'misc/abbreviations/data/french_abbreviation_dict.xlsx' 
xlsx = pd.ExcelFile(file_path)

# Function to convert a DataFrame into an Esri Maplex abbreviation file format
def create_abbreviation_file(sheet_name, df):
    # Create a file name based on the sheet name
    file_name = f"{sheet_name}_abbreviation.dic"
    
    # Open file for writing with ASCII encoding (plaintext)
    with open(file_name, 'w', encoding='ascii') as file:
        # Write the header comments
        file.write("* Maplex Label Engine Dictionary File - v1.0\n")
        file.write("* Format: TEXT ABBREVIATION(S) TYPE\n")
        file.write("* where TYPE=[Translation|Keyword|Ending]\n\n")
        
        # Iterate through DataFrame rows and write each abbreviation entry
        for index, row in df.iterrows():
            word = row[0].strip()  # Strip any leading/trailing spaces
            abbreviation = row[1].strip()  # Ensure no spaces in the abbreviation
            abbrev_type = row[2].strip().upper()  # Convert type to uppercase
            
            # Write the line in the required format, ensuring no extra spaces
            file.write(f'"{word}" {abbreviation} {abbrev_type}\n')
        
        # Write the end comment
        file.write("\n* [end]\n")

# Iterate through each sheet in the Excel file
for sheet_name in xlsx.sheet_names:
    df = pd.read_excel(xlsx, sheet_name)
    create_abbreviation_file(sheet_name, df)

print("Dictionary files have been created.")
