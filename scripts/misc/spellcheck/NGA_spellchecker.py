import pandas as pd
import re
from textblob import TextBlob

# Load the spreadsheet
file_path = '/Users/matthewheaton/Downloads/nhfr_facility_spelling.xlsx'
data = pd.read_excel(file_path)

# Function to detect, clean, and correct English words using TextBlob
def correct_and_clean(word):
    # Remove non-letter characters except apostrophes
    clean_word = re.sub(r"[^A-Za-z']", '', word)
    
    # Skip empty entries
    if not clean_word:
        return None
    
    # Detect if the word is likely English with a high confidence threshold
    blob = TextBlob(clean_word)
    correction_suggestions = blob.words[0].spellcheck()
    
    # Check if the word is likely English and has a high similarity confidence
    if correction_suggestions[0][1] > 0.85 and correction_suggestions[0][0] == clean_word:
        # Populate "word_eng" if confirmed as English
        data.at[index, 'word_eng'] = clean_word
        return None  # The word is correct; no change needed
    
    # If the word is similar to English but likely misspelled
    elif correction_suggestions[0][1] > 0.65:
        corrected_word = str(blob.correct())
        if corrected_word != clean_word:
            print(f"Original: {word} -> Corrected: {corrected_word}")
            return corrected_word  # Populate "word_corrected" if it's misspelled
    
    # Return None if the word is non-English or already correct
    return None

# Initialize the new "word_eng" column
data['word_eng'] = None

# Apply the function to each word in the "words" column
for index, word in data['words'].items():
    data.at[index, 'word_corrected'] = correct_and_clean(word)

# Save the result back to a new Excel file
output_file_path = '/Users/matthewheaton/Downloads/nhfr_facility_spelling_corrected.xlsx'
data.to_excel(output_file_path, index=False)

print("Processing complete! Check the output file for results.")
