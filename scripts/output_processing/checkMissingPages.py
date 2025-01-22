import pandas as pd

def join_excel_files(master_file, results_file, output_file):
    # Load the Excel files into DataFrames
    master_df = pd.read_excel(master_file)
    results_df = pd.read_excel(results_file)

    # Ensure the 'Key_master' and 'Key_results' columns exist in the respective files
    if 'Key_master' not in master_df.columns:
        raise ValueError("The master file must contain a 'Key_master' column.")
    if 'Key_results' not in results_df.columns:
        raise ValueError("The results file must contain a 'Key_results' column.")

    # Normalize the key columns (strip whitespace, convert to lowercase)
    master_df['Key_master'] = master_df['Key_master'].astype(str).str.strip().str.lower()
    results_df['Key_results'] = results_df['Key_results'].astype(str).str.strip().str.lower()

    # Perform the join (left join to retain all rows from master_df)
    joined_df = pd.merge(
        master_df, 
        results_df, 
        left_on='Key_master', 
        right_on='Key_results', 
        how='left'
    )

    # Identify rows in the results list that did not match the master list
    unmatched_df = results_df[~results_df['Key_results'].isin(master_df['Key_master'])]

    # Save the results to an Excel file
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        joined_df.to_excel(writer, sheet_name='Joined Data', index=False)
        unmatched_df.to_excel(writer, sheet_name='Unmatched Results', index=False)

    print(f"Joined data and unmatched results have been written to {output_file}")

if __name__ == "__main__":
    # Example usage
    master_file = r"E:\\mheaton\\cartography\\COD_EAF_reference_microplanning_consolidation_20241121\\OUTPUT_A2_microplanification_20241213_rename\\Mapindex_ExportTable_20241219.xlsx"
    results_file = r"E:\\mheaton\\cartography\\COD_EAF_reference_microplanning_consolidation_20241121\\OUTPUT_A2_microplanification_20241213_rename\\OUTPUT_A2_microplanification_20241213_rename_report_20250103.xlsx"
    output_file = r"E:\\mheaton\\cartography\\COD_EAF_reference_microplanning_consolidation_20241121\\OUTPUT_A2_microplanification_20241213_rename\\joined_data_report.xlsx"

    join_excel_files(master_file, results_file, output_file)
    print(f"Results saved to {output_file}")
