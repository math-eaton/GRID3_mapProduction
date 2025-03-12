import os
import shutil
from datetime import datetime

# Configuration
input_folder = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\OUTPUT_A2_microplanification_20241213"   # Folder where your input files are located
output_folder = r"E:\mheaton\cartography\COD_EAF_reference_microplanning_consolidation_20241121\OUTPUT_A2_microplanification_20241213_rename" # Folder where you want to put renamed files
date_str = datetime.now().strftime('%Y%m%d')  # Use current date or a fixed string like "20241214"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    # Skip directories
    if os.path.isdir(os.path.join(input_folder, filename)):
        continue
    
    name, ext = os.path.splitext(filename)
    parts = name.split("_")
    
    # Check if it matches the known input template of 7 parts:
    # pagesize_usecase_country_province_antenna_healthZone_healthArea
    if len(parts) != 7:
        # Not matching template, skip
        continue
    
    pagesize, usecase, country, province, antenna, healthZone, healthArea = parts
    
    # Example transformations:
    # Convert all to uppercase (except maybe keep some original casing if desired)
    # The example output seems to use uppercase fields except perhaps the page size might be uppercase too.
    # Adjust as needed.
    pagesize   = pagesize.upper()
    usecase    = usecase.lower()  # maybe the usecase stays lower, adjust as needed
    country    = country.upper()
    province   = province.upper()
    antenna    = antenna.upper()
    healthZone = healthZone.upper()
    healthArea = healthArea.upper()
    
    # Rearrange into the final pattern:
    # pagesize_country_province_antenna_healthZone_healthArea_usecase_DATE.ext
    new_basename = f"{pagesize}_{country}_{province}_{antenna}_{healthZone}_{healthArea}_{usecase}_{date_str}"
    new_filename = new_basename + ext
    
    # Handle duplicates: if the file exists, append a counter
    counter = 1
    final_path = os.path.join(output_folder, new_filename)
    while os.path.exists(final_path):
        final_path = os.path.join(output_folder, f"{new_basename}_{counter}{ext}")
        counter += 1
    
    # Copy (or move) the file to the output folder with the new name
    # Use shutil.move(...) if you want to move instead of copying
    shutil.copy(os.path.join(input_folder, filename), final_path)

print("Renaming completed.")
