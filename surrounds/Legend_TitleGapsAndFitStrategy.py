# Author:  Esri
# Date:    March 2020
# Version: ArcGISPro 2.5
# Purpose: This script alters a Legend's title, fitting strategy, and gaps.
# Notes:   The script is intended to work from a script tool provided with
#          a sample project using "CURRENT".  To see the changes happen be
#          sure to active the appropriate map or layout.

p = arcpy.mp.ArcGISProject('current')
lyt = p.listLayouts('GreatLakes')[0]

cim_lyt = lyt.getDefinition('V2')     #Get the layout's CIM definition

#Iterate though all layout elements to find the Legend element
for elm in cim_lyt.elements:
  if elm.name == "Legend":

    #Legend Title
    elm.title = "The Great Lakes Area"
    elm.titleSymbol.symbol.horizontalAlignment = 'Center'
    elm.titleSymbol.symbol.smallCaps = True

    #Get everything to fit in the envelope
    elm.fittingStrategy = "AdjustFonts"
    elm.minFontSize = 4
    elm.columns = 3

    #Legend level changes
    elm.titleGap = 20
    elm.horizontalPatchGap = 5
    elm.verticalItemGap = 5

lyt.setDefinition(cim_lyt)            #Set the layout's CIM definition
