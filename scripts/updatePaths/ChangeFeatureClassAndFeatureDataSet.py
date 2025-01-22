# Author:  Esri
# Date:    March 2020
# Version: ArcGISPro 2.5
# Purpose: This script changes the data source of a layer to point to a 
#          different feature class in a different File Geodatabase in a different
#          Feature Dataset.
# Notes:   - The script is intended to work from a script tool provided with
#            a sample project using "CURRENT".  To see the output of the script, be
#            sure to view the appropriate map.
#          - The output of the script can be viewed by looking at the layers's properties > Source

p = arcpy.mp.ArcGISProject('current')
m = p.listMaps('DataSources')[0]
l = m.listLayers('US States')[0]

# Specify the new geodatabase, feature class and feature dataset
newGDB = "FGDB2.gdb"
newFeatureClass = "states2"
newFeatureDataSet = "USA2"

# Get the layer's CIM definition
lyrCIM = l.getDefinition('V2')         
dc = lyrCIM.featureTable.dataConnection

# Change the connection string to point to the new File Geodatabase
dc.workspaceConnectionString = dc.workspaceConnectionString.replace("FGDB.gdb", newGDB)

# Change the dataset name
dc.dataset = newFeatureClass

# If the data is in a Feature Dataset, then update it 
if hasattr(dc, "featureDataset"):
    dc.featureDataset = newFeatureDataSet

# Set the layer's CIM definition
l.setDefinition(lyrCIM)
