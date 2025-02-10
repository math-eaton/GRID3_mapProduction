# script to interpret and reformat country-specific thoroughfare and other abbreviations 
# based on the UNIVERSAL POSTAL UNION (APO) dictionary PDF https://www.upu.int/

import pandas as pd
import re

def sanitize_sheet_name(name):
    """Sanitize the sheet name to remove invalid characters and ensure it's no longer than 31 characters."""
    return re.sub(r'[\\/*?:[\]]', '_', name)[:31]  # Replace invalid characters with underscores, limit to 31 characters

def split_by_delimiter(input_file, output_file, delimiter='64'):
    """Splits the input Excel file based on the delimiter, creating separate sheets."""
    # Load the data from the Excel file
    df = pd.read_excel(input_file, sheet_name=None)
    
    # Extract the first sheet (assuming it's the one with data)
    sheet_name = list(df.keys())[0]
    data = df[sheet_name]
    
    sections = {}
    current_section = []
    current_sheet_name = None
    
    # Iterate through the rows to identify the delimiter pattern and split sections
    for index, row in data.iterrows():
        row_text = ' '.join([str(item).strip() for item in row if pd.notnull(item)])  # Combine non-null items, stripping spaces
        
        if delimiter in row_text:
            # Save the previous section to the dictionary when a new delimiter is found
            if current_sheet_name and current_section:
                # Grab the first three characters of the first cell in the section for the sheet name
                sheet_name_from_first_cell = sanitize_sheet_name(str(current_section[0][0])[:3])
                sections[sheet_name_from_first_cell] = pd.DataFrame(current_section)
            
            # Start a new section
            current_sheet_name = row_text
            current_section = []
        
        else:
            # Add non-empty rows to the current section
            if any(pd.notnull(item) for item in row):
                # Ensure each cell's value is stripped of extra spaces
                current_section.append([str(item).strip() if pd.notnull(item) else '' for item in row.tolist()])
    
    # Save the last section
    if current_sheet_name and current_section:
        sheet_name_from_first_cell = sanitize_sheet_name(str(current_section[0][0])[:3])
        sections[sheet_name_from_first_cell] = pd.DataFrame(current_section)
    
    # Write all sections to a new Excel file, each in a separate sheet
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        for sheet_name, section_data in sections.items():
            # Convert everything to plain values without formatting
            section_data.fillna('', inplace=True)  # Replace NaN with empty strings for clean output
            section_data.to_excel(writer, sheet_name=sheet_name, index=False)

def clean_data(input_file):
    """Cleans each sheet by deleting empty columns, empty rows, and using the second row as the header."""
    # Load the data from the Excel file
    df = pd.read_excel(input_file, sheet_name=None)

    # Define the output file with "_intermediate" suffix
    output_file = input_file.replace('.xlsx', '_intermediate.xlsx')

    # Create a writer object for the new file
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        # Process each sheet
        for sheet_name, sheet_data in df.items():
            # Delete empty columns
            sheet_data_cleaned = sheet_data.dropna(how='all', axis=1)
            
            # Delete empty rows
            sheet_data_cleaned = sheet_data_cleaned.dropna(how='all', axis=0)
            
            # Check if the first column is empty or has only whitespace, then remove it
            if sheet_data_cleaned.iloc[:, 0].apply(lambda x: isinstance(x, str) and x.strip() == '' or pd.isna(x)).all():
                sheet_data_cleaned = sheet_data_cleaned.drop(sheet_data_cleaned.columns[0], axis=1)
            
            # Use the second row as the header and drop it from the data
            sheet_data_cleaned.columns = sheet_data_cleaned.iloc[1]
            sheet_data_cleaned = sheet_data_cleaned.drop(sheet_data_cleaned.index[:2])  # Drop first two rows
            
            # Ensure that the data is plain, without any formatting
            sheet_data_cleaned.fillna('', inplace=True)  # Replace NaN with empty strings
            
            # Write cleaned data to the new file
            sheet_data_cleaned.to_excel(writer, sheet_name=sheet_name, index=False)

    return output_file

# step 1 - format input
input_file = 'misc/abbreviations/data/thoroughfare_abbreviations_forMaps.xlsx'
output_file = 'misc/abbreviations/data/thoroughfare_abbreviations_forMaps_ISO-SPLIT.xlsx'
split_by_delimiter(input_file, output_file)

# step 2 - cleaning whitespace
cleaned_file = clean_data(output_file)
