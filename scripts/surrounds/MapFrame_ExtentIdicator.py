# Author:  Esri
# Date:    March 2020
# Version: ArcGISPro 2.5
# Purpose: #This script updates the symbology for an extent indicator.
# Notes:   The script is intended to work from a script tool provided with
#          a sample project using "CURRENT".  To see the changes happen be
#          sure to active the appropriate map or layout.


p = arcpy.mp.ArcGISProject('current')
lyt = p.listLayouts('GreatLakes')[0]

lyt_cim = lyt.getDefinition('V2')     #Get the Layout's CIM definition

#Iterate though all layout elements to find the MapFrame element
for elm in lyt_cim.elements:
  if elm.name == "Locator MF":
    for ei in elm.extentIndicators:
      if ei.name == "Extent of Great Lakes MF":
        symLyr = ei.symbol.symbol.symbolLayers[0]  #Get solid stroke 
        symLyr.color.values = [255, 0, 0, 100]     #Change color to red
        symLyr.width = 3                           #Change outline width

lyt.setDefinition(lyt_cim)            #Set the Layout's CIM definition
