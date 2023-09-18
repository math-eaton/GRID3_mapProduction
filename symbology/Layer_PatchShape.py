# Author:  Esri
# Date:    March 2020
# Version: ArcGISPro 2.5
# Purpose: This script modifies the patch shape associated with each layer.
# Notes:   - The script is intended to work from a script tool provided with
#            a sample project using "CURRENT".  To see the changes happen be
#            sure to active the appropriate map or layout.
#          - Changing a layer's patch shape will also affect a legend that
#            displays the layer.

p = arcpy.mp.ArcGISProject('current')
lyt = p.listLayouts('GreatLakes')[0]
m = p.listMaps('GreatLakes')[0]

#Iterate through each layer in the map
for lyr in m.listLayers():            #Get the layer's CIM definition
  cim_lyr = lyr.getDefinition('V2')

  if lyr.name == "GreatLakes":
    cim_lyr.renderer.patch = "AreaHydroPoly"  #Change patch for single symbol

  if lyr.name == "States" or lyr.name == "Provinces":
    for grp in cim_lyr.renderer.groups:       #Iterate through each group
      for cls in grp.classes:                 #Iterate through each class
        cls.patch = "AreaBoundary"            #Change patch for the class
        
  lyr.setDefinition(cim_lyr)          #Set the layer's CIM definition

