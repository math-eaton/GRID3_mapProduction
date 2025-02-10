import arcpy
import os

def delete_feature_classes_with_substring(gdb_path, substring):
    """ Delete all feature classes containing the substring in the specified geodatabase """
    arcpy.env.workspace = gdb_path
    # List all feature classes, including those within feature datasets
    for dataset in arcpy.ListDatasets() + ['']:  # include root and datasets
        for feature_class in arcpy.ListFeatureClasses(feature_dataset=dataset):
            if substring in feature_class:
                # Construct the path to the feature class
                feature_class_path = os.path.join(gdb_path, feature_class)
                arcpy.Delete_management(feature_class_path)
                print(f"Deleted feature class: {feature_class_path}")

def process_geodatabases(directory, substring):
    """ Process all geodatabases in the directory to delete specified feature classes """
    for filename in os.listdir(directory):
        if filename.endswith(".gdb"):
            gdb_path = os.path.join(directory, filename)
            delete_feature_classes_with_substring(gdb_path, substring)

if __name__ == "__main__":
    directory = r'C:\path\to\directory'  # Directory containing geodatabases
    substring = "KSPH_"  # Substring to look for in feature class names

    # Optionally, specify a single geodatabase path instead
    gdb_path = r'E:\mheaton\cartography\COD_microplanning_042024\data\consolidated\consolidated.gdb'
    # 
    delete_feature_classes_with_substring(gdb_path, substring)

    # Process all geodatabases in the specified directory
    # process_geodatabases(directory, substring)
