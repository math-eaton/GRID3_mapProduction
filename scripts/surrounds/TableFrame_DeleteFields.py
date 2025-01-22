# Author:  Esri
# Date:    March 2020
# Version: ArcGISPro 2.5
# Purpose: This script will remove/hide fields from the TableFrame.  It will
#          also set the width of the remaining fields.
# Notes:   The script is intended to work from a script tool provided with
#          a sample project using "CURRENT".  To see the changes happen be
#          sure to active the appropriate map or layout.

p = arcpy.mp.ArcGISProject('current')
lyt = p.listLayouts('GreatLakes')[0]

lyt_cim = lyt.getDefinition("V2")     #Get the layout's CIM definition

#Iterate though all layout elements to find the TableFrame element
for elm in lyt_cim.elements:
  if elm.name == "Table Frame":
    #Remove fields in reverse order to avoid skipping elements while iterating
    for f in reversed(elm.fields):
        if f.name == "PageNumNorm" or f.name == "Rotation" or f.name == "Scale":
          elm.fields.remove(f)
        else:
          f.width = 150               #Set the width to 150 pixels

lyt.setDefinition(lyt_cim)            #Get the layout's CIM definition
