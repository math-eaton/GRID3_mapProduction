# Author:  Esri
# Date:    March 2020
# Version: ArcGISPro 2.5
# Purpose: This script modifies field heading symbols and field text, changes
#          alternating row symbols and modifies other root level TableFrame
#          properties.
# Notes:   The script is intended to work from a script tool provided with
#          a sample project using "CURRENT".  To see the changes happen be
#          sure to active the appropriate map or layout.

p = arcpy.mp.ArcGISProject('current')
lyt = p.listLayouts('GreatLakes')[0]

lyt_cim = lyt.getDefinition("V2")     #Get the layout's CIM definition

#Iterate though all layout elements to find the TableFrame element
for elm in lyt_cim.elements:
  if elm.name == "Table Frame":

    #Modify Heading symbols and field text
    for f in elm.fields:
      #Set all headings to be red and center aligned
      f.headingTextSymbol.symbol.symbol.symbolLayers[0].color.values = [255,0,0,100]
      f.headingTextSymbol.symbol.horizontalAlignment = 'Center'

      #Set the values for NAME to be blue and center aligned
      if f.name == "NAME":
        f.textSymbol.symbol.symbol.symbolLayers[0].color.values = [0,0,255,100]
        f.textSymbol.symbol.horizontalAlignment = 'Center'

    #Modify other root level properties
    elm.horizontalTextGap = 25
    elm.headingGap = 10
    elm.headingLineSymbol.symbol.symbolLayers[0].color.values = [0,0,255,100]
    elm.headingLineSymbol.symbol.symbolLayers[0].width = 2

    #Change the alternate row background configuration
    elm.alternate1RowBackgroundCount = 1
    elm.alternate2RowBackgroundCount = 1
    elm.alternate2RowBackgroundSymbol.symbol.symbolLayers[0].color.values = [190, 210, 255, 100]

lyt.setDefinition(lyt_cim)            #Set the layout's CIM definition
