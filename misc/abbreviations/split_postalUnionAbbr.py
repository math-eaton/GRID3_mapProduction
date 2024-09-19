# script to interpret and reformat country-specific thoroughfare and other abbreviations 
# based on the UNIVERSAL POSTAL UNION (APO) dictionary PDF https://www.upu.int/


import pandas as pd
import re

def sanitize_sheet_name(name):
    """Replace invalid characters in sheet names."""
    return re.sub(r'[\\/*?:[\]]', '_', name)  # Replaces any invalid characters with an underscore

def split_by_delimiter(input_file, output_file, delimiter='64'):
    # Load the data
    df = pd.read_excel(input_file, sheet_name=None)
    
    # Extract the first sheet (assuming there's only one relevant sheet)
    sheet_name = list(df.keys())[0]
    data = df[sheet_name]
    
    sections = {}
    current_section = []
    current_sheet_name = None
    
    # Iterate through the rows to identify the delimiter pattern and split sections
    for index, row in data.iterrows():
        row_text = ' '.join([str(item) for item in row if pd.notnull(item)])  # Combine non-null items as a string
        
        if delimiter in row_text:
            # Save the previous section to the dictionary when a new delimiter is found
            if current_sheet_name and current_section:
                # Grab the first three characters of the first cell in the section for the sheet name
                sheet_name_from_first_cell = sanitize_sheet_name(str(current_section[0][0])[:3])
                sections[sheet_name_from_first_cell] = pd.DataFrame(current_section)
            
            # Start a new section
            current_sheet_name = row_text  # Name the new sheet by the first 3 characters of this row
            current_section = []
        
        else:
            # Add non-empty rows to the current section
            if any(pd.notnull(item) for item in row):
                current_section.append(row.tolist())
    
    # Save the last section
    if current_sheet_name and current_section:
        sheet_name_from_first_cell = sanitize_sheet_name(str(current_section[0][0])[:3])
        sections[sheet_name_from_first_cell] = pd.DataFrame(current_section)
    
    # Write all sections to a new Excel file, each in a separate sheet
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        for sheet_name, section_data in sections.items():
            section_data.to_excel(writer, sheet_name=sheet_name, index=False)


input_file = 'misc/abbreviations/data/thoroughfare_abbreviations_forMaps.xlsx'
output_file = 'misc/abbreviations/data/thoroughfare_abbreviations_forMaps_ISO-SPLIT.xlsx'
split_by_delimiter(input_file, output_file)
