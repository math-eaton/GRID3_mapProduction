# Author:  Esri
# Date:    March 2020
# Version: ArcGISPro 2.5
# Purpose: This script modifies the number of columns and the font associated
#          with paragraph text.
# Notes:   The script is intended to work from a script tool provided with
#          a sample project using "CURRENT".  To see the changes happen be
#          sure to active the appropriate map or layout.

p = arcpy.mp.ArcGISProject('current')
lyt = p.listLayouts('GreatLakes')[0]

lyt_cim = lyt.getDefinition("V2")     #Get the layout's CIM definition

#Iterate though all layout elements to find the ParagraphcText element
for elm in lyt_cim.elements:
  if elm.name == "Paragraph Text":
    elm.graphic.columnCount = 2
    elm.graphic.columnGap = 15        #Points, the UI is in pages units
    elm.graphic.symbol.symbol.fontStyleName = 'Trebuchet MS'
    elm.graphic.symbol.symbol.symbol.symbolLayers[0].color.values = [0,0,255,100]
    elm.graphic.symbol.symbol.indentFirstLine = 15
    elm.graphic.symbol.symbol.horizontalAlignment = "Justify"

lyt.setDefinition(lyt_cim)            #Set the layout's CIM definition

